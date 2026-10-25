#!/bin/sh
# Assemble the .deb for OSK-Keyboard.
#
# Run from the project root on a Debian/Ubuntu host (needs dpkg-deb).
# Produces dist/osk-keyboard_<ver>_<arch>.deb from the files already in this
# repo, so the package can never drift from the source tree.
#
# Before 1.0.1b the package was called opd2413-keyboard; the new name carries
# Conflicts/Replaces so a plain `apt install` migrates cleanly.
set -e

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PKG=osk-keyboard
STAGE="$ROOT/packaging/$PKG"
DIST="$ROOT/dist"

VER=$(sed -n 's/^Version: *//p' "$STAGE/DEBIAN/control" | head -1)
ARCH=$(sed -n 's/^Architecture: *//p' "$STAGE/DEBIAN/control" | head -1)
[ -n "$VER" ] || { echo "cannot read Version from control" >&2; exit 1; }
[ -n "$ARCH" ] || { echo "cannot read Architecture from control" >&2; exit 1; }
DEB="$DIST/${PKG}_${VER}_${ARCH}.deb"

echo "=== staging $PKG $VER ==="
rm -rf "$STAGE/usr" "$DIST"
mkdir -p \
    "$STAGE/usr/share/gnome-shell/extensions/erhai-osk@local" \
    "$STAGE/usr/bin" \
    "$STAGE/usr/share/applications" \
    "$DIST"

cp "$ROOT/scripts/erhai-osk-ext/extension.js" \
   "$ROOT/scripts/erhai-osk-ext/metadata.json" \
   "$STAGE/usr/share/gnome-shell/extensions/erhai-osk@local/"

cp "$ROOT/scripts/osk-keyboard-toggle.sh" \
   "$STAGE/usr/bin/osk-keyboard"

cp "$ROOT/scripts/osk-keyboard.desktop" \
   "$STAGE/usr/share/applications/osk-keyboard.desktop"

# dpkg-deb preserves the tree's modes, so set them explicitly.
# The DEBIAN directory itself must be 0755: a tree that came in from Windows or
# from a FAT/exFAT volume arrives as 0707, and dpkg-deb refuses to build.
chmod 755 "$STAGE/DEBIAN"
chmod 755 "$STAGE/usr/bin/osk-keyboard"
chmod 755 "$STAGE/DEBIAN/postinst" "$STAGE/DEBIAN/postrm"
chmod 644 "$STAGE/usr/share/applications/osk-keyboard.desktop"
chmod 644 "$STAGE/usr/share/gnome-shell/extensions/erhai-osk@local/"*.js \
          "$STAGE/usr/share/gnome-shell/extensions/erhai-osk@local/"*.json

echo "=== tree ==="
find "$STAGE" -path "$STAGE/DEBIAN" -prune -o -print | sed "s|$STAGE|.|" | sort

# The maintainer scripts carry the version literally (debhelper would do this
# via #VERSION#; we substitute by hand to avoid a debhelper dependency).
sed -i "s/@VERSION@/$VER/g" "$STAGE/DEBIAN/postinst"

echo "=== build $DEB ==="
dpkg-deb --build --root-owner-group "$STAGE" "$DEB"

echo "=== result ==="
ls -l "$DEB"
dpkg-deb --info "$DEB"
echo
dpkg-deb --contents "$DEB"
