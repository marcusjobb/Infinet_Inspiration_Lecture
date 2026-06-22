#!/usr/bin/env bash
# Triggers screenpipe captures on Linux by simulating window focus changes.
# Screenpipe npm CLI on Linux only captures on AT-SPI2 window events, not on
# idle timer. This script forces a focus-switch every INTERVAL seconds so
# screenpipe captures continuously without user interaction.
#
# Run in a separate terminal alongside screenpipe:
#   bash scripts/screenpipe-trigger.sh

INTERVAL=${1:-15}

echo "🔁 Screenpipe trigger — fönsterbyte var ${INTERVAL}s"
echo "   Avsluta med Ctrl+C"
echo ""

while true; do
    sleep "$INTERVAL"

    CURRENT=$(xdotool getactivewindow 2>/dev/null)
    if [ -z "$CURRENT" ]; then
        continue
    fi

    # Find a real app window to briefly focus (skip gnome-shell which opens Activities)
    OTHER=$(xdotool search --onlyvisible --name "" 2>/dev/null | grep -v "^${CURRENT}$" | while read wid; do
        wclass=$(xdotool getwindowclassname "$wid" 2>/dev/null)
        if [ -n "$wclass" ] && [ "$wclass" != "Gnome-shell" ] && [ "$wclass" != "gnome-shell" ]; then
            echo "$wid"
            break
        fi
    done)

    if [ -n "$OTHER" ]; then
        xdotool windowfocus --sync "$OTHER" 2>/dev/null
        sleep 0.15
        xdotool windowfocus --sync "$CURRENT" 2>/dev/null
        echo "$(date '+%H:%M:%S') capture trigger ✓"
    else
        echo "$(date '+%H:%M:%S') inget annat fönster att byta till"
    fi
done
