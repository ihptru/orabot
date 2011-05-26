#!/bin/sh
log=./botlog.txt
while true; do
	./orabot.py &> $log &
	tail -f $log &
	wait %1
	echo "Server has crashed. It will restart immediately..., press CTRL-C to cancel"
	sleep 5
done
