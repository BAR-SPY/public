#!/bin/bash

devs=($(
	bluetoothctl list devices \
		| sed -nre 's/.*dev_([0-9A-F_]+).*/\1/p' \
		| uniq \
		| tr "_" ":"
	))

for d in "${devs[@]}"; do
	bluetoothctl info $d \
		| grep -Eo "(Name:.*|Paired:.*|Connected:.*)"
done
