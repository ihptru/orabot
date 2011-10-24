# Copyright 2011 orabot Developers
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

"""
Check if website is down
"""

import config
import urllib.request
import re

def check_localnetwork(self, url):
    if re.search('127.*', url):
        return True
    if re.search('192.168.*', url):
        return True
    if url == 'localhost':
        return True
    if re.search('10\..*', url):
        return True
    return False

def usage(self, user):
    usage = "Usage: " + config.command_prefix + "isdown <url>"
    self.send_notice(usage, user)

def isdown(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 2 ):
        url = command[1].split('://')
        if ( len(url) == 1 ):
            if check_localnetwork(self, url[0]):
                self.send_notice("Can't check local network", user)
                return
            url = 'http://' + url[0]
        else:
            if check_localnetwork(self, url[1]):
                self.send_notice("Can't check local network", user)
                return
            url = command[1]
        try:
            urllib.request.urlopen(url)
            self.send_reply( (url + " Is Up"), user, channel)
        except urllib.error.URLError:
            self.send_reply( (url + " Is Down"), user, channel)
    else:
        usage(self, user)
        return
