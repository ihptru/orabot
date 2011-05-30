#!/usr/bin/env python3
## This script restarts the server every time it is crashing.

import io
import sys
import time
import os
import orabot

try:
    os.mkdir("run")
except OSError as e:
    if e.args[0]==17:   #Run already exists
        pass    #Ignore
    else:
        raise e #Raise exception again

os.chdir("run")

logfile="botlog.txt"
log=io.open(logfile,"a")

# a class which works like the shell command "tee"
class Tee(io.TextIOWrapper):
    def __init__(self, f1, f2):
        io.TextIOWrapper.__init__(self, f1)
        self.f1=f1
        self.f2=f2
        self.buffered1=False
        self.buffered2=False
    def write(self, text):
        self.f1.write(text)
        self.f2.write(text)
        if not self.buffered1:
            self.f1.flush()
        if not self.buffered2:
            self.f2.flush()

# a class for flushed output
class FlushFile(io.TextIOWrapper):
    def __init__(self, f):
        io.TextIOWrapper.__init__(self, f)
        self.f=f
    def write(self, text):
        self.f.write(text)
        self.f.flush()

sys.stdout=Tee(sys.stdout, log)
sys.stderr=FlushFile(sys.stderr)    #Allways flush stderr
print("Starting bot. Press ctrl+c to exit.")
while(True):
    try:
        orabot.main()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Bot has crashed. Restarting it in 5 seconds.")
        sys.stderr.write("Exception: " + e.__class__.__name__ + "(" + str(e) + ")\n")
        try:
            time.sleep(5) # Wait 5 seconds, so if the bot crashes on every time, it doesn't spam the console.
            continue # Restart
        except KeyboardInterrupt: # User pressed ctrl+c
            break # Quit main loop
    break #Break if not restarted.
