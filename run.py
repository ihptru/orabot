#!/usr/bin/env python3
## This script restarts the server every time it is crashing.

import threading
import io
import sys

logfile="botlog.txt"
log=io.open(logfile,"a")

# a class which works like the shell command "tee"
class Tee(io.TextIOWrapper):
	def __init__(self, f1, f2):
		self.f1=f1
		self.f2=f2
		self.buffered1=False
		self.buffered2=False
	def write(self, text):
		self.f1.write(text)
		#self.f2.write(text)
		if not self.buffered1:
			self.f1.flush()
		if not self.buffered2:
			self.f2.flush()

sys.stdout=Tee(sys.stdout, log)
print("Starting bot. Press ctrl+c to exit.")
while(True):
	try:
		import orabot
	except KeyboardInterrupt:
		break
	except Exception as e:
		print("Bot has crashed. Restarting it NOW.")
		sys.stderr.write("Exception: " + e.__class__.__name__ + "(" + str(e) + ")")

print("Quit.")
sys.stdout=sys.__stdout__
