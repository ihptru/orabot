#!/usr/bin/env python3
#
# Copyright 2011-2013 orabot Developers
#
# This file is part of orabot, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import sys
import time
import os
import gzip
import shutil
import orabot

try:
    os.mkdir("var")
except OSError as e:
    if e.args[0]==17:   #Directory already exists
        pass    #Ignore
    else:
        raise e #Raise exception again

try:
    os.mkdir("db")
    os.chmod("db", 0o700)
except OSError as e:
    if e.args[0]==17:   #Directory already exists
        pass    #Ignore
    else:
        raise e #Raise exception again

logfile = "var/botlog.txt"
log = io.open(logfile, "a")

# a class which works like the shell command "tee"
class Tee(io.TextIOWrapper):

    def __init__(self, f1, f2, fd):
        io.TextIOWrapper.__init__(self, f1)
        self.f1 = f1
        self.f2 = f2
        self.fd = fd

    def write(self, text):
        if (text.strip() != ''):
            text = time.strftime('[%Y-%m-%d %H:%M:%S] ') + text
        self.f1.write(text)
        self.f2.write(text)
        self.f1.flush()
        self.f2.flush()
        # next bit of code is for log rotation
        if self.fd == "stdout":
            log_f = open('var/botlog.txt')
            log_f_lines = log_f.readlines()
            if len(log_f_lines) > 10000:
                _files = []
                _dir = os.listdir('var/')
                for fn in _dir:
                    if fn[0:6] == "botlog":
                        _files.append(fn)
                _nums = []
                for file in _files:
                    if file == "botlog.txt":
                        _nums.append(0)
                    else:
                        _nums.append(int(file.split("botlog")[1].split(".")[0]))
                _nums.sort()
                _nums.reverse()
                #gzip
                for num in _nums:
                    if num != 0:
                        source = "var/botlog"+str(num)+".txt.gz"
                        dest = "var/botlog"+str(num+1)+".txt.gz"
                        shutil.move(source, dest)
                    else:
                        f_in = open('var/botlog.txt', 'rb')
                        f_out = gzip.open('var/botlog1.txt.gz', 'wb')
                        f_out.writelines(f_in)
                        f_out.close()
                        f_in.close()
                        self.f2.close()
                        open('var/botlog.txt', 'w').close()
                        self.f2 = io.open('var/botlog.txt', 'a')

sys.stdout=Tee(sys.stdout, log, "stdout")
sys.stderr=Tee(sys.stderr, log, "stderr")
print("Starting bot. Press CTRL+C to exit.")

while(True):
    try:
        orabot.main()
    except KeyboardInterrupt:
        break
    break #Break if not restarted.
