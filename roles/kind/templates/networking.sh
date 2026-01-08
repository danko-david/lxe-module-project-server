#!/bin/bash

set -e

KIND_IP=$(docker inspect {{ HOST_DNS_NAME }}-control-plane | jq -r ".[0].NetworkSettings.Networks.kind.IPAddress")

# route for k8s network for traefik

	MANAGED_ROUTES=$(route -n | grep -P '^10\.244\.0\.0\s+172\.\d+\.\d+\.\d+' || true)

	# if theres only one route and it is matching ok, if not, remove all and add route
	if ! [ $(wc -l <<< $MANAGED_ROUTES) == 1 ] || ! grep -q $KIND_IP <<< $MANAGED_ROUTES
	then
		if [ ! -z "$MANAGED_ROUTES" ]
		then
			while read -ra l
			do
				route del -net ${l[0]} netmask ${l[2]} gw ${l[1]}
			done <<< "$MANAGED_ROUTES"
		fi
		route add -net 10.244.0.0/16 gw $KIND_IP
	fi

# Manage Port redirects

if ! iptables-save | grep -q -- '-A FORWARD -j ACCEPT'
then
	iptables -t filter -I FORWARD 1 -j ACCEPT
fi

RULES=$(iptables-save | grep -- "-A PREROUTING -p tcp" || true)

# if ip changed (or no record)
if [ $(grep $KIND_IP <<< "$RULES" | wc -l ) != 2 ]
then
	while read -ra l
	do
		if [ ! -z "$l" ]
        then
			iptables -t nat $(sed 's/-A PREROUTING/-D PREROUTING/' <<< "${l[@]}")
		fi
	done <<< "$RULES"

	iptables -t nat -A PREROUTING -p tcp --dport 6443 -j DNAT --to "$KIND_IP":6443
	iptables -t nat -A PREROUTING -p tcp --dport 30000:32767 -j DNAT --to "$KIND_IP":30000-32767
fi
