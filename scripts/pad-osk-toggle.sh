#!/bin/sh
# PAD-OSK -- show/hide the on-screen keyboard.
#
# This drives the SAME state as the Quick Settings switch, through
# ~/.config/erhai-osk/visible (the extension watches that file).  The earlier
# version toggled `gnome-extensions enable/disable`, a second, independent axis:
# after hiding the keyboard from the system menu, the icon's first tap only
# disabled an already-hidden extension, so it took two taps to see anything.
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/1000}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=/run/user/1000/bus}"

UUID=erhai-osk@local
CFG="${XDG_CONFIG_HOME:-$HOME/.config}/erhai-osk"
STATE="$CFG/visible"

if ! command -v gnome-extensions >/dev/null 2>&1; then
    echo "gnome-extensions not found" >&2
    exit 1
fi

mkdir -p "$CFG"

# If the extension itself is off (e.g. disabled from the Extensions app), turn it
# on and show the keyboard -- that is what tapping the icon should mean.
if ! gnome-extensions list --enabled 2>/dev/null | grep -qx "$UUID"; then
    printf '1' > "$STATE"
    gnome-extensions enable "$UUID" && echo "keyboard on (extension enabled)"
    exit 0
fi

CUR=1
[ -f "$STATE" ] && CUR=$(cat "$STATE" 2>/dev/null || echo 1)

if [ "$CUR" = "1" ]; then
    printf '0' > "$STATE"
    echo "keyboard off"
else
    printf '1' > "$STATE"
    echo "keyboard on"
fi
