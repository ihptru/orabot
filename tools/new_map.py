# Copyright 2011-2015 orabot Developers
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
    cached_hash = ""
    while  True:
        time.sleep(3660)  # wait an hour and 1 minute
        cached_hash = detect(self, cached_hash)

def detect(self, cached_hash):
    url = 'http://resource.openra.net/map/lastmap/'
    try:
        stream = self.data_from_url(url, None)
    except Exception as e:
        print(("*** [%s] %s: %s") % (self.irc_host, __name__, e))
        return cached_hash

    y = json.loads(stream)
    if cached_hash == "":
        cached_hash = y[0]['map_hash']
        return cached_hash
    if cached_hash != y[0]['map_hash']:
        cached_hash = y[0]['map_hash']
        self.send_message_to_channel('New map: %s by %s | %s' % (y[0]['title'], y[0]['author'], 'http://resource.openra.net/maps/'+str(y[0]['id'])+'/'), '#openra')
    return cached_hash