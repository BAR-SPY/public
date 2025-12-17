#!/bin/bash

git_folder="${HOME}\/personal\/"

git_status=$( cd "$git_folder" && git status | grep -Eo "nothing to commit, working tree clean" )
git_push_status=$( cd "$git_folder" && git status | grep -Eo "Your branch.*$" | grep -Eo "[0-9]" )

if [[ ! -z "$git_status" && -z $git_push_status ]]; then
	printf "{\"text\": \"Git: %s\"}\n" "Clean"
	exit 0
elif [[ ! -z "$git_push_status" ]]; then
	printf "{\"text\": \"Git: %s\"}\n" "Push needed. $git_push_status commit(s) ahead."
else
	printf "{\"text\": \"Git: %s\"}\n" "Commit needed. $git_folder"
	exit 0
fi

