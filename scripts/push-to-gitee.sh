#!/bin/sh
# Push the on-screen-keyboard project to Gitee.
#
#   sh scripts/push-to-gitee.sh https://gitee.com/<user>/opd2413-keyboard.git
#
# Run from the project root. Needs git. Only this project's files are added;
# everything else in the project root stays out of the repository.
set -e

REMOTE="$1"
[ -n "$REMOTE" ] || { echo "usage: $0 <gitee-remote-url>" >&2; exit 1; }

case "$REMOTE" in
    https://*|git@*) ;;
    *) echo "not a git remote url: $REMOTE" >&2; exit 1 ;;
esac

cd "$(dirname "$0")/.."
echo "repo root: $(pwd)"

command -v git >/dev/null 2>&1 || { echo "git is required" >&2; exit 1; }

# whitelist-style ignore: our project only, nothing else in this tree
cat > .gitignore <<'IGNORE'
# This repository carries only the on-screen keyboard project.
# Everything else in the working tree is ignored (whitelist style).
*
!.gitignore
!LICENSE
!/README.md
!/PUSH-TO-GITEE.md
!/packaging/
!/scripts/
!/docs/
!/dist/

# scripts/: only the keyboard files
/scripts/*
!/scripts/erhai-osk-ext/
!/scripts/opd2413-keyboard-toggle.sh
!/scripts/opd2413-keyboard.desktop

# docs/: only the keyboard write-up
/docs/*
!/docs/屏幕键盘-方案.md

# build intermediates (DEBIAN/postinst gets its version substituted)
/packaging/opd2413-keyboard/usr/

# dist/: ship the .deb, nothing else
/dist/*
!/dist/*.deb

# OS / editor noise
Thumbs.db
desktop.ini
.vscode/
*.swp
*~
IGNORE
echo "wrote .gitignore (whitelist mode)"

if [ ! -f LICENSE ]; then
    echo
    echo "NOTE: no LICENSE file. Before publishing publicly, add one"
    echo "      (MIT or GPL-3.0); without it all rights are reserved."
    echo
fi

# ---- git init --------------------------------------------------------
if [ ! -d .git ]; then
    git init -q
    echo "initialised repository"
fi

for p in LICENSE README.md PUSH-TO-GITEE.md packaging scripts/erhai-osk-ext \
         scripts/opd2413-keyboard-toggle.sh scripts/opd2413-keyboard.desktop \
         docs/屏幕键盘-方案.md dist; do
    if [ -e "$p" ]; then
        git add -- "$p"
    else
        echo "skip (missing): $p"
    fi
done
git add -- .gitignore

echo
echo "=== files to be committed ==="
git status --short
echo

if [ -n "$(git diff --cached --name-only)" ]; then
    NAME=${GIT_AUTHOR_NAME:-opd2413}
    MAIL=${GIT_AUTHOR_EMAIL:-opd2413@local}
    git -c "user.name=$NAME" -c "user.email=$MAIL" commit -q \
        -m "opd2413-keyboard 1.0: GNOME 50 Wayland on-screen keyboard"
    echo "committed"
else
    echo "nothing to commit"
fi

BRANCH=main
CURRENT=$(git rev-parse --abbrev-ref HEAD)
[ "$CURRENT" = "$BRANCH" ] || git branch -M "$BRANCH"

if git remote | grep -qx origin; then
    git remote set-url origin "$REMOTE"
    echo "updated origin -> $REMOTE"
else
    git remote add origin "$REMOTE"
    echo "added origin -> $REMOTE"
fi

echo
echo "pushing to $REMOTE ($BRANCH)"
echo "authenticate with your Gitee username + a personal access token:"
echo "  https://gitee.com/profile/personal_access_tokens"
git push -u origin "$BRANCH"

echo
echo "done."
