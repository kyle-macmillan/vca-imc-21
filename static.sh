#!/bin/bash

TRACE=$1
ROUTER=$2

echo "Reading trace $TRACE"

sleep 1

for i in {1..5}
do
	while IFS= read -r line
	do
		echo $line	
		a=( $line )
		echo "Setting ${a[1]} down and ${a[2]} up"
		ssh -n $ROUTER "./shaper.sh start ${a[1]} ${a[2]} 0 0"
		python3 test.py teams 150 -i en4 -id https://teams.microsoft.com/l/meetup-join/19%3a9f85bdc95a344cd29c346f51f3c6be29%40thread.tacv2/1632759553702?context=%7b%22Tid%22%3a%2283b02c92-5f26-48ed-9e5b-6c2fca46a8e6%22%2c%22Oid%22%3a%22099d321a-faad-4c74-9352-3da45ada8fcf%22%7d -r ${a[1]}-${a[2]} 
		sleep 1
		ssh -n $ROUTER "./shaper.sh stop"
		
	done < $TRACE
done
