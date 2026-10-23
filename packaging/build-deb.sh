#!/bin/sh
# Assemble a .deb for the OPD2413 on-screen keyboard.
#
# Run from the project root on a Debian/Ubuntu host (needs dpkg-deb).
# Produces dist/opd2413-keyboard_<ver>_all.deb from the files already in this
# repo, so the package can never drift from the source tree.
set -e

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PKG=opd2413-keyboard
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

cp "$ROOT/scripts/opd2413-keyboard-toggle.sh" \
   "$STAGE/usr/bin/opd2413-keyboard"

cp "$ROOT/scripts/opd2413-keyboard.desktop" \
   "$STAGE/usr/share/applications/opd2413-keyboard.desktop"

# dpkg-deb preserves the tree's modes, so set them explicitly.
chmod 755 "$STAGE/usr/bin/opd2413-keyboard"
chmod 755 "$STAGE/DEBIAN/postinst" "$STAGE/DEBIAN/postrm"
chmod 644 "$STAGE/usr/share/applications/opd2413-keyboard.desktop"
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
