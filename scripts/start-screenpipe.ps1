# =============================================================================
# Screenpipe startskript — Windows (PowerShell)
# =============================================================================
# Minne: 6 månader
#   --retention-mode media  -> OCR-text och transkriptioner bevaras i 180 dagar
#                              men video/ljud/bild-filer rensas löpande
#                              -> disken sprängs inte, minnena lever kvar
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
    --retention-days 180 `
    --retention-mode media `
    --video-quality low `
    --language swedish `
    --filter-music `
    --disable-clipboard-capture `
    @IgnoreArgs
