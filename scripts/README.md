# Scripts

Startskript för Screenpipe på olika plattformar.

## Filer

| Fil | Plattform | Beskrivning |
|-----|-----------|-------------|
| `start-screenpipe.sh` | Linux / macOS | Rekommenderat startskript med säkerhetsinställningar |
| `start-screenpipe.ps1` | Windows | Samma inställningar för PowerShell |
| `restart-screenpipe.sh` | Linux / macOS | Stoppar och startar om Screenpipe |
| `screenpipe-trigger.sh` | Linux / macOS | Triggar en manuell capture |
| `vanilla.sh` | Linux / macOS | Minimal start utan flaggor — för felsökning |

## Starta på Linux / macOS

```bash
chmod +x start-screenpipe.sh
./start-screenpipe.sh
```

## Starta på Windows

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\start-screenpipe.ps1
```

## Inställningar i start-screenpipe.sh / .ps1

| Inställning | Värde | Varför |
|-------------|-------|--------|
| `--retention-days 1` | 1 dag | Video/bild raderas snabbt — sparar disk |
| `--retention-mode media` | media | OCR-text bevaras i 180 dagar |
| `--video-quality low` | låg | Minskar CPU och diskåtgång |
| `--disable-audio` | av | Andras röster fångas inte |
| `--disable-clipboard-capture` | av | Lösenord passerar clipboard |
| `--disable-keyboard-capture` | av | Tangenttryckningar loggas inte |
| `--visual-check-interval-ms 5000` | 5 sek | Capture var 5:e sekund |

## Blockerade fönster

Redigera `IGNORED_WINDOWS`-listan i `start-screenpipe.sh` för att lägga till appar som aldrig ska fångas (t.ex. lösenordshanterare, bankapp).

## Felsökning

Kör `vanilla.sh` för att starta Screenpipe utan några extra flaggor. Lägg sedan till en flagga i taget och starta om — på så sätt hittar du vilken inställning som orsakar problem.
