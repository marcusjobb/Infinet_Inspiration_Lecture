#!/usr/bin/env bash
pkill -f "screenpipe record" 2>/dev/null
sleep 2

exec screenpipe record \
    --retention-days 1 \
    --retention-mode media \
    --video-quality low \
    --language swedish \
    --language english \
    --disable-audio \
    --disable-clipboard-capture \
    --disable-keyboard-capture \
    --ignored-windows "1Password::" \
    --ignored-windows "Bitwarden::" \
    --ignored-windows "KeePass::" \
    --ignored-windows "Secrets::" \
    --ignored-windows "Enpass::" \
    --idle-capture-interval-ms 15000 \
    --visual-check-interval-ms 5000
