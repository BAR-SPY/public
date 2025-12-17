#!/bin/bash

# This is a script to perform a system audit and email it.
# It utilizes a Lynis full system audit and a "warnings-only" 
# as well as chkrootkit to generate the report.
#
# msmtp is setup to mail the report.

LYNIS_FULL="/var/log/lynis/full/lynis.full.$(date +%Y%m%d-%H%M%S).log"
LYNIS_WARN="/var/log/lynis/warnings-only/lynis.warn.$(date +%Y%m%d-%H%M%S).log"
CHKROOTKIT="/var/log/chkrootkit/chkrootkit.$(date +%Y%m%d-%H%M%S).log"
REPORT="/var/log/system-audit/system-audit-report.$(date +%Y%m%d-%H%M%S).out"

function mail(){
	sudo -u ahamrick msmtp -C /home/ahamrick/.config/msmtp/config -t -a proton-xyz < $1 
}	

if [[ $(id -u) -ne 0 ]]; then echo "This script must be run as root."; exit 255; fi

if [[ ! -d /var/log/lynis/full ]]; then
	mkdir -pv /var/log/lynis/full
elif [[ ! -d /var/log/lynis/warnings-only ]]; then
	mkdir -pv /var/log/lynis/warnings-only
elif [[ ! -d /var/log/system-audit ]]; then
	mkdir -pv /var/log/system-audit
elif [[ ! -d /var/log/chkrootkit ]]; then
	mkdir -pv /var/log/chkrootkit
elif [[ ! -f $REPORT ]]; then
	touch $REPORT
fi

# Lynis System Audits
lynis audit system --cron-job >> $LYNIS_FULL
lynis audit system --cron-job --warnings-only &>> $LYNIS_WARN

# chkrootkit
chkrootkit &>> $CHKROOTKIT

# Getting report together

cat <<-EOF >> $REPORT
To: austin@hamrick.xyz
From: austin@hamrick.xyz
Subject: System Audit $(date +%Y%m%d)
System Audit Generated: $(date +%Y%m%d-%H%M%S).

########################################
#	Lynis Warnings Only            #
########################################
$( cat  $LYNIS_WARN )

For a full report, view $LYNIS_FULL

########################################
# 	chkrootkit results	       #
########################################

Not Infected: $( cat $CHKROOTKIT | grep -Eo "Checking.*not infected" | wc -l)
Rootkits NOT Found: $( cat $CHKROOTKIT | grep -Eo "Searching for.*" | wc -l)

File Scan:
$( cat $CHKROOTKIT | grep -Eo "Checking.*not infected" )

Rootkit Scan:
$( cat $CHKROOTKIT | grep -Eo "Searching for.*" )
EOF

mail $REPORT
