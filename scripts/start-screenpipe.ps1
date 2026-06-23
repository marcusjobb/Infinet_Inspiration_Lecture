# =============================================================================
# Screenpipe startskript — Windows (PowerShell)
# =============================================================================
# Minne: text och OCR bevaras i 180 dagar (6 månader)
#   --retention-days 1      -> video/bild/ljud raderas redan efter 1 dag
#                              (så fort Screenpipe har skrivit av dem behövs de inte)
#   --retention-mode media  -> OCR-text och transkriptioner bevaras däremot
#                              i hela 180 dagar — minnena lever kvar utan att
#                              disken sprängs
#
# Redigera listan nedan för att blockera appar du aldrig vill att Screenpipe
# ska se (t.ex. din lösenordshanterare, bankapp, etc.)
# =============================================================================

$IgnoredWindows = @(
    "1Password::"
    "Bitwarden::"
    "KeePass::"
    "Enpass::"
    "LastPass::"
)

$IgnoreArgs = $IgnoredWindows | ForEach-Object { @("--ignored-windows", $_) }

& screenpipe record `
    --retention-days 1 `
    --retention-mode media `
    --video-quality low `
    --language swedish `
    --language english `
    --disable-audio `
    --disable-clipboard-capture `
    --disable-keyboard-capture `
    --disable-ui-monitoring `
    --visual-check-interval-ms 5000 `
    @IgnoreArgs
