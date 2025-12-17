#!/usr/bin/python3
############################################################
# Helper script to search and replace CCs                  #
############################################################

import subprocess
import os

def s_and_r(filename, search, replace):
	with open(filename, 'r') as f:
		file_content = f.read()

	modified_content = file_content.replace(search, replace)

	with open(filename, 'w') as f:
		f.write(modified_content)
	f.close()

def process_number(number):
	number_str = str(number)
	if len(number_str) < 16:
		return number_str
	else:
		stripped=f"{number_str[:6]}-xx-{number_str[-4:]}"
		return stripped

"""
	This section will likely need to be modified to do the following:
	1. Handle multiple entries. [x]
	2. Handle the matches from the dlp_mailscan output.

Example of command line to handle this:

cd /var/spool/ && \
  for f in *.eml; do cat $f \ 
  | dlp_mailscan -v \
  | grep -Eo "Match:.*$" \
  | sed -nre 's/Match:(.*)$/\1/p'; done
"""

command = """
for f in *.txt; do cat $f | grep -Eo [0-9]{16};done
"""

"""
	The below is to check for files with the extension in the endswith
	It can be expanded to check more directories if needed.
"""
file_w_extension = [file for file in os.listdir(".") if file.endswith("txt")]

output = subprocess.check_output(command, shell=True, text=True)
# Split lines was chosen here since it outputs a dictionary
output_str = output.splitlines()

"""
	The below for loop may need to be refactored, as it currently
	will check for ALL entries in "output_str" in whichever file is 
	in "f".
	This could prove to be dangerous as it could find both in one file.
	It inherently shouldn't be considered a high severity, as even if it does 
	find both, the context of this script is to censor CCs in a file and 
	both of them should be censored anyways.
"""
for f in file_w_extension:
	for cmd_f in output_str:
		result = process_number(cmd_f)
		s_and_r(f, cmd_f, result)
		print(f"Clear: {cmd_f}; Censored: {result}")


