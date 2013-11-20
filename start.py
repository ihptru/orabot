#!/usr/bin/env python3

# Copyright 2011-2014 orabot Developers
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

import sys
import os
import gzip
import shutil
import orabot

try:
    os.mkdir("var") # Create directory for temp files and logs
    os.mkdir("db")  # Create directory where database is stored
    os.chmod("db", 0o700)
except OSError as e:
    if e.args[0] == 17:   # Directory already exists
        pass    # Ignore
    else:
        raise e # Raise exception again

# a class which works like the shell command "tee"
class Tee:
    def __init__(self, fd, logfile):
        self.fd = fd
        self.logfile = logfile

    def __del__(self):
        self.logfile.close()

    def write(self, text):
        self.fd.write(text)
        self.logfile.write(text)
        self.log_rotate(text)

    def flush(self):
        self.fd.flush()
        self.logfile.flush()

    def log_rotate(self, text):
        log_file = open('var/console_log.txt')
        log_file_lines = log_file.readlines()
        if len(log_file_lines) > 100000:
            _files = []
            _dir = os.listdir('var/')
            for filename in _dir:
                if filename[0:11] == 'console_log':
                    _files.append(filename)
            _nums = []
            for file in _files:
                if file == "console_log.txt":
                    _nums.append(0)
                else:
                    _nums.append(int(file.split('console_log_')[1].split('.')[0]))
            _nums.sort()
            _nums.reverse()
            for number in _nums:
                if number != 0:    # rename every existing log file
                    source = 'var/console_log_'+str(number)+'.txt.gz'
                    dest = 'var/console_log_'+str(number+1)+'.txt.gz'
                    shutil.move(source, dest)
                else:   # gzip last one
                    shutil.copy('var/console_log.txt', 'var/console_log_1.txt')
                    file_to_gz = open('var/console_log_1.txt', 'rb')
                    result_gz_file = gzip.open('var/console_log_1.txt.gz', 'wb')
                    result_gz_file.writelines(file_to_gz)
                    result_gz_file.close()
                    file_to_gz.close()
                    os.remove("var/console_log_1.txt")
                    open('var/console_log.txt', 'w').close()

logfile = "var/console_log.txt"
log = open(logfile, "a")

sys.stdout = Tee(sys.stdout, log)
sys.stderr = Tee(sys.stderr, log)
print("Starting bot. Press CTRL+C to exit.")

orabot.main()
