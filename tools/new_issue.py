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

import time
import urllib.request
import json

def start(self):
    if self.irc_host != "irc.freenode.net":
        return
    time.sleep(1800)    # wait 30 minutes
    y = bugs_list(self) # request a list from github
    e_bugs = [n['number'] for n in y]
    
    while True:
        time.sleep(1800)    # wait 30 minutes
        e_bugs = detect_bugs(self, e_bugs)

def detect_bugs(self, e_bugs):
    y = bugs_list(self) # request a list from github
    remote_bugs = [n['number'] for n in y]
    
    for bug in remote_bugs:
        if bug not in e_bugs:   # it's a new bug
            e_bugs.append(bug)
            type = "issue"
            if remote_bugs.index(bug)['pull_request']['html_url'] != None:
                type = "pull request"
            self.send_message_to_channel(("New %s #%s by %s: %s | http://bugs.open-ra.org/%s")
                                        % (type, str(bug), y[remote_bugs.index(bug)]['user']['login'],
                                        y[remote_bugs.index(bug)]['title'], str(bug)), "#openra")
    return e_bugs

def bugs_list(self):
    url = 'https://api.github.com/repos/OpenRA/OpenRA/issues'
    while True:
        try:
            data = urllib.request.urlopen(url).read().decode()
            return json.loads(data)
        except:
            print("*** [%s] Could not fetch a list of OpenRA bugs, apparently 'Exceed Rate Limit'" % self.irc_host)
            time.sleep(7200)    # wait 2 hours
