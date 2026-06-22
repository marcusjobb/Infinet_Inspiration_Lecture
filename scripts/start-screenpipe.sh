#!/usr/bin/env bash
# =============================================================================
# Screenpipe startskript — Linux / macOS
# =============================================================================
# Minne: text och OCR bevaras i 180 dagar (6 månader)
#   --retention-days 1      → video/bild/ljud raderas redan efter 1 dag
#                             (så fort Screenpipe har skrivit av dem behövs de inte)
#   --retention-mode media  → OCR-text och transkriptioner bevaras däremot
#                             i hela 180 dagar — minnena lever kvar utan att
#                             disken sprängs
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
    --retention-days 1 \
    --retention-mode media \
    --video-quality low \
    --language swedish \
    --filter-music \
    --disable-clipboard-capture \
    "${IGNORE_ARGS[@]}"
