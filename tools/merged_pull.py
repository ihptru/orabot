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
import json

def start(self):
    if self.irc_host != "irc.freenode.net":
        print("*** [%s] Terminating child process (unsupported): %s" % (self.irc_host, __name__))
        return
    cached = False
    while  True:
        time.sleep(2520)  # wait 42 minutes
        cached = detect(self, cached)

def detect(self, cached):
    pulls = pulls_list(self)
    if not pulls:
        return False
    if not cached:
        return pulls[0]['number']

    for pull in pulls:
        if pull['number'] == cached:
            break
        if not pull['merged_at']:
            continue
        self.send_message_to_channel("Merged lately (%s %s) PR created by %s: %s | http://bugs.openra.net/%s" % (pull['merged_at'].split('T')[0], pull['merged_at'].split('T')[1].split('Z')[0], pull['user']['login'], pull['title'], pull['number']), "#openra")
    return pulls[0]['number']

def pulls_list(self):
    url = 'https://api.github.com/repos/OpenRA/OpenRA/pulls?state=closed'
    try:
        data = urllib.request.urlopen(url).read().decode()
        return json.loads(data)
    except:
        print("*** [%s] Could not fetch a list of OpenRA bugs, apparently 'Exceed Rate Limit'" % self.irc_host)
        time.sleep(7200)    # wait 2 hours
        return False
