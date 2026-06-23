import os, sys, time, json, re, subprocess, tempfile
from datetime import datetime
import easyocr

# Matchar eye.py:s egna utskriftsrader som kan dyka upp i OCR av terminalen
_EYE_LINE = re.compile(
    r'[✓·⇄⏱=¥—]\s*\d*\s*(tecken|skip|tom)?\s*\[|'
    r'\bEYE_\w+\s*=|'
    r'@ Eye\b|'
    r'Loggar till.*\.eye|'
    r'Avsluta med Ctrl',
    re.IGNORECASE,
)

INTERVAL  = int(os.getenv("EYE_INTERVAL", "15"))
EYE_DIR   = os.path.expanduser("~/.eye")
LOG_FILE  = os.path.join(EYE_DIR, "log.jsonl")
SNAP      = os.path.join(tempfile.gettempdir(), "eye_snap.png")
SKIP_APPS = {s.lower() for s in os.getenv("EYE_SKIP", "kitty").split(",") if s}
VERBOSE   = os.getenv("EYE_VERBOSE", "0") == "1"

os.makedirs(EYE_DIR, exist_ok=True)

print("👁  Laddar OCR-modell...", flush=True)
_reader = easyocr.Reader(["sv", "en"], gpu=False, verbose=False)
print("   Klar.\n", flush=True)


def active_window_class() -> str:
    wid = subprocess.run(
        ["xdotool", "getactivewindow"], capture_output=True, text=True,
    ).stdout.strip()
    if not wid:
        return "unknown"
    # xprop ger "WM_CLASS(STRING) = \"instans\", \"Klass\""
    result = subprocess.run(
        ["xprop", "-id", wid, "WM_CLASS"], capture_output=True, text=True,
    )
    if result.returncode == 0 and '"' in result.stdout:
        parts = result.stdout.split('"')
        cls = parts[3] if len(parts) >= 4 else parts[1]
        return cls.lower()
    # Fallback: fönsternamnet
    name = subprocess.run(
        ["xdotool", "getwindowname", wid], capture_output=True, text=True,
    ).stdout.strip()
    return name.lower() or "unknown"


def screenshot() -> bool:
    result = subprocess.run(["scrot", "--overwrite", SNAP], capture_output=True)
    if result.returncode != 0:
        result = subprocess.run(["gnome-screenshot", "-f", SNAP], capture_output=True)
    return result.returncode == 0


def ocr() -> str:
    results = _reader.readtext(SNAP)
    raw = "\n".join(r[1] for r in results)
    clean = "\n".join(l for l in raw.splitlines() if not _EYE_LINE.search(l))
    return clean.strip()


_last_text = {}  # app → senast sparade text, för att hoppa över dubbletter

BROWSER_APPS = {"chrome", "chromium", "firefox", "brave", "brave-browser", "msedge", "edge"}
_URL_RE = re.compile(r'https?://[^\s"\'<>]+')


def extract_url(text: str) -> str | None:
    m = _URL_RE.search(text)
    return m.group(0).rstrip(".,)") if m else None


def capture():
    app = active_window_class()
    if app in SKIP_APPS:
        if VERBOSE:
            print(f"— skip  [{app}]")
        return
    if not screenshot():
        print("[fel] screenshot misslyckades")
        return
    text = ocr()
    if not text:
        if VERBOSE:
            print(f"· (tom)  [{app}]")
        return
    if _last_text.get(app) == text:
        if VERBOSE:
            print(f"· (oförändrad)  [{app}]")
        return
    _last_text[app] = text
    entry = {"ts": datetime.now().isoformat(timespec="seconds"), "app": app, "text": text}
    if any(b in app for b in BROWSER_APPS):
        url = extract_url(text)
        if url:
            entry["url"] = url
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    url_hint = f"  {entry['url']}" if "url" in entry else ""
    print(f"✓ {len(text)} tecken  [{app}]  {entry['ts']}{url_hint}")


def get_active_wid() -> str:
    return subprocess.run(
        ["xdotool", "getactivewindow"], capture_output=True, text=True,
    ).stdout.strip()


print("\033c", end="", flush=True)
print(f"👁  Eye  ·  fönsterbyte + var {INTERVAL}s")
print(f"   Loggar till {LOG_FILE}  (format: tid | app | text)")
print("   Avsluta med Ctrl+C\n")

prev_wid    = None
last_capture = 0.0

while True:
    try:
        now = time.time()
        wid = get_active_wid()
        window_switched  = wid != prev_wid and wid != ""
        interval_elapsed = now - last_capture >= INTERVAL

        if window_switched or interval_elapsed:
            trigger = "⇄" if window_switched else "⏱"
            print(trigger, end=" ", flush=True)
            capture()
            prev_wid    = wid
            last_capture = now

        time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nHejdå!")
        sys.exit(0)
    except Exception as e:
        print(f"[fel] {e}")
        time.sleep(1)
