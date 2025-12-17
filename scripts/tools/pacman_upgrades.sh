#!/bin/bash

function usage(){
cat <<EOF
$0 [-l| -t | -u | -j]
	-l : list packages available for upgrade.
	-t : get total number of packages available for upgrade
	-u : update packages. Requires sudo.
	-j : show output in JSON format.
EOF
}

function update_packages(){
	log="/var/log/pacman_upgrades"
	# Refresh pacman
	[[ $(id -u)  -eq 0 ]] && echo "[+] Syncing Packages... $(date +%Y%m%d-%H%M%S)" >> $log && pacman -Sy >> $log
	echo "[=] $(pacman -Qu | wc -l) Packages With Updates available." >> $log
	pacman -Qu >> $log 
}

function get_total(){
	total=$( pacman -Qu | wc -l)
	
	if [[ $total -eq 0 ]]; then
		echo "𜱭"
	else
		echo "↥ $total"
	fi
}

function get_list(){
	list=$( pacman -Qu | sed -re ':a;N;$!ba;s/\n/\\n/g' )

	if [[ -z $list ]]; then
		echo "No packages available for upgrade."
	else
		echo -n "$list"
	fi
}

function json_out(){
	printf "{\"text\": \"%s\", \"tooltip\": \"%s\"}" "$(get_total)" "$(get_list)"
	#printf "{\"text\": \"%s\", \"tooltip\": \"%s\"}" "$(get_total)" "testing"
	#printf "{\"text\": \"%s\"}\n" "$(get_total)"
}

while getopts "ltuj" opt; do
	case $opt in
		l) get_list;;
		t) get_total;;
		u) update_packages;;
		j) json_out;;
		*|?) echo "Invalid argument."; usage;;
	esac
done
if [[ $OPTIND -eq 1 ]]; then
	echo "No arguments passed."
	usage
	exit 1
fi

