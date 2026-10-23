#!/bin/sh
# Sync the GitHub mirror from local master.
#
# Why this exists: the two repositories are published under different identities
# so that each platform links the commits to the maintainer's own account and no
# platform's no-reply address leaks into the other.
#
#   Gitee  小鸟游星野 <HOSHINO6@users.noreply.gitee.com>
#   GitHub ホシノ     <186796588+HOSHINO61@users.noreply.github.com>
#
# A commit carries only one author, so the trees are identical while the SHAs
# differ. This script rebuilds branch 'gh' by replaying master linearly with the
# GitHub identity, then force-pushes it to the GitHub remote.
#
# Usage:  sh scripts/sync-github.sh [--push]
set -e

GH_NAME="ホシノ"
GH_MAIL="186796588+HOSHINO61@users.noreply.github.com"
REMOTE="github"
BRANCH="master"

git rev-parse --verify "$BRANCH" >/dev/null 2>&1 || {
    echo "error: branch '$BRANCH' not found" >&2
    exit 1
}

prev=""
first=""
for c in $(git rev-list --reverse "$BRANCH"); do
    tree=$(git rev-parse "$c^{tree}")
    when=$(git log -1 --format=%aI "$c")

    export GIT_AUTHOR_NAME="$GH_NAME"
    export GIT_AUTHOR_EMAIL="$GH_MAIL"
    export GIT_COMMITTER_NAME="$GH_NAME"
    export GIT_COMMITTER_EMAIL="$GH_MAIL"
    export GIT_AUTHOR_DATE="$when"
    export GIT_COMMITTER_DATE="$when"

    if [ -z "$prev" ]; then
        prev=$(git log -1 --format=%B "$c" | git commit-tree "$tree")
        first="$prev"
    else
        prev=$(git log -1 --format=%B "$c" | git commit-tree "$tree" -p "$prev")
    fi
done

git branch -f gh "$prev"

echo "gh built at $prev"
echo "v1.0 commit  $first"
echo "--- history ---"
git log --format="%h %an <%ae>  %s" -4 gh

echo "--- tree matches master? ---"
if [ "$(git rev-parse gh^{tree})" = "$(git rev-parse "$BRANCH^{tree}")" ]; then
    echo "yes"
else
    echo "NO - aborting" >&2
    exit 1
fi

if [ "$1" = "--push" ]; then
    git push "$REMOTE" "gh:$BRANCH" --force
    git push "$REMOTE" "$first:refs/tags/v1.0" --force
    echo "pushed to $REMOTE"
else
    echo
    echo "dry run; re-run with --push to update $REMOTE"
fi
