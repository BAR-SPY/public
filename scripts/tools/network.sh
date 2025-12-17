#!/bin/bash

status=$( ip -o a s up | grep -v ^1 )

connected_to=$( nmcli | grep -i "connected to" | sed -nre 's/.*:.*connected to(.*)/\1/p' )
dev=$( nmcli | grep -i "connected to" | sed -nre 's/^(.*):.*$/Connected using \1/p' )

if [[ "$dev" ]]; then
	if [[ $dev =~ wlan ]]; then
		echo "{\"text\": \"ᯤ $connected_to\",\"tooltip\":\"$dev\"}"
	elif [[ $dev =~ en ]]; then
		echo "{\"text\": \" $connected_to\",\"tooltip\":\"$dev\"}"
	elif [[ -z $dev ]]; then
		echo "{\"text\": \"No Connection.\"}"
	fi
fi
