#!/usr/bin/env bash
# =============================================================================
# Screenpipe startskript — Linux / macOS
# =============================================================================
# Minne: 6 månader
#   --retention-mode media  → OCR-text och transkriptioner bevaras i 180 dagar
#                             men video/ljud/bild-filer rensas löpande
#                             → disken sprängs inte, minnena lever kvar
#
# Redigera listan nedan för att blockera appar du aldrig vill att Screenpipe
# ska se (t.ex. din lösenordshanterare, bankapp, etc.)
# =============================================================================

IGNORED_WINDOWS=(
    "1Password::"
    "Bitwarden::"
    "KeePass::"
    "Secrets::"
    "Enpass::"
)

IGNORE_ARGS=()
for w in "${IGNORED_WINDOWS[@]}"; do
    IGNORE_ARGS+=(--ignored-windows "$w")
done

exec screenpipe record \
    --retention-days 180 \
    --retention-mode media \
    --video-quality low \
    --language swedish \
    --filter-music \
    --disable-clipboard-capture \
    "${IGNORE_ARGS[@]}"
