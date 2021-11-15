#!/bin/bash

while (( "$#" )); do
  case "$1" in
    --URL)
      FORKED_URL=$2
      shift 2
      ;;
    --USER)
      USER=$2
      shift 2
      ;;
    --STRATEGY)
      STRATEGY=$2
      shift 2
      ;;
    --AUTH)
      AUTH_TOKEN=$2
      shift 2
      ;;
    *)
      echo Unsupport argument $1
      exit 1
      ;;
  esac
done

git config --global user.name "${USER}"
git config --global user.email "${USER}@users.noreply.github.com"

git pull --unshallow

# Need to remove 'https://'
FORKED_URL="${FORKED_URL:8}"

FORKED_URL="https://x-access-token:${AUTH_TOKEN}@${FORKED_URL}"

git remote add upstream "${FORKED_URL}"
git fetch upstream

git remote -v

git checkout upstream/main

LABS_TO_UPDATE=$(cat automation/labs.txt)

if [[ "$STRATEGY" == 'keep_upstream' ]]; then
  # Merge in favour of the original repository

  git merge --strategy-option theirs --no-edit origin/main

  for lab in $LABS_TO_UPDATE; do

    git checkout origin/main -- lab_"${lab}"/start.py
    git checkout origin/main -- lab_"${lab}"/main.py

  done

  git commit -m "checkout labs from the origin repository"

elif [[ "$STRATEGY" == 'keep_fork' ]]; then
  # Merge in favour of the forked repository

  git merge --strategy-option ours --no-edit origin/main

  for lab in $LABS_TO_UPDATE; do

    git checkout upstream/main -- lab_"${lab}"/start.py
    git checkout upstream/main -- lab_"${lab}"/main.py

  done

  git commit -m "get latest changes from the original repository"

else
  # Just get the latest changes from the original repository
  git merge --no-edit origin/main
fi

DIFF=$(git diff --name-only HEAD@{0} HEAD@{1})

echo ::set-output name=files_diff::"${DIFF}"

git push upstream HEAD:main
