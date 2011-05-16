#!/bin/sh
log=botlog.txt
while true; do
	./orabot.py | tee -a $log
	echo "Server has crashed. It will restart immediately..., press CTRL-C to cancel"
	sleep 5
done
