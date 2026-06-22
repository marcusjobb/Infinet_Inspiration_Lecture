import os, sys, time, json, subprocess, tempfile
from datetime import datetime

INTERVAL  = int(os.getenv("EYE_INTERVAL", "15"))
EYE_DIR   = os.path.expanduser("~/.eye")
LOG_FILE  = os.path.join(EYE_DIR, "log.jsonl")
SNAP      = os.path.join(tempfile.gettempdir(), "eye_snap.png")
LANGS     = "swe+eng"

os.makedirs(EYE_DIR, exist_ok=True)


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
    result = subprocess.run(
        ["tesseract", SNAP, "stdout", "-l", LANGS, "--psm", "3"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        result = subprocess.run(
            ["tesseract", SNAP, "stdout", "-l", "eng", "--psm", "3"],
            capture_output=True, text=True,
        )
    return result.stdout.strip()


def capture():
    app = active_window_class()
    if not screenshot():
        print("[fel] screenshot misslyckades")
        return
    text = ocr()
    if text:
        entry = {"ts": datetime.now().isoformat(timespec="seconds"), "app": app, "text": text}
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"✓ {len(text)} tecken  [{app}]  {entry['ts']}")
    else:
        print(f"· (tom)  [{app}]")


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
