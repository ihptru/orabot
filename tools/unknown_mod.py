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
    while  True:
        time.sleep(7320)  # wait 2 hours and 2 minutes
        detect(self)

def detect(self):
    url = 'http://master.openra.net/games_json'
    try:
        stream = self.data_from_url(url, None)
    except Exception as e:
        print(("*** [%s] %s: %s") % (self.irc_host, __name__, e))
        return

    y = json.loads(stream)
    for item in y:
        if item['mods'].split('@',1)[0] not in ['ra', 'cnc', 'td', 'd2k', 'ts'] and item['state'] == '1' and int(item['players']) >= 1:
            self.send_message_to_channel( "Detected a waiting game with unknown mod: %s | players: %s" % (item['mods'], item['players']), "#openra")
