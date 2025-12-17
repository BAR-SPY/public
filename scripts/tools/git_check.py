#!/usr/bin/python3

import os
import subprocess
import json
import re

git_folder = os.path.expanduser("~/personal")

def run_git_command(command):
    try:
        result = subprocess.run(
                command, cwd=git_folder, capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Git command failed: ", e)
        return ""

# Check Git Status
git_status_output = run_git_command(["git", "status"])
is_clean = re.search(r"nothing to commit, working tree clean", git_status_output)

# Branch Status
branch_status = re.search(r"Your branch is ahead of.*by (\d+) commit", git_status_output)
ahead_commits = branch_status.group(1) if branch_status else None

#Modified tooltip
porcelain_out = run_git_command(["git", "status", "--porcelain"])
modified_files = []
for line in porcelain_out.strip().splitlines():
    # This is to search for modified files only.
    status_code = line[:2]
    file_path = line[2:]
    if "M" or "A" or "??" in status_code:
        modified_files.append(file_path)

files_modified = "\n".join(modified_files) if modified_files else None

#Determine output.
if is_clean and not ahead_commits:
    print(json.dumps({"text": "Git: ✅"}))
elif ahead_commits:
    if modified_files:
        print(json.dumps({
            "text": f"🔼 🟡 Git:{ahead_commits} commit(s) ahead.",
            "tooltip": f"Modified Files\n {files_modified}"
            }))
    else:
        print(json.dumps({
            "text": f"🔼 Git: {ahead_commits} commit(s) ahead.",
            "tooltip": f"No further files modified."
            }))
else:
    print(json.dumps({
        "text": f"🔼 🟡 Git: Commit needed.", 
        "tooltip": f"Modified Files:\n {files_modified}"
        }))
