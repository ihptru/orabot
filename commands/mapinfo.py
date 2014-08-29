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

"""
Shows the full openra map's information; search by title
"""

import json
import urllib.request

def mapinfo(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 1 ):
        self.send_reply( ("Part of map's name required!"), user, channel )
    else:
        map_pattern = "%20".join(command[1:])
        url = "http://resource.openra.net/map/title/%s" % map_pattern
        data = urllib.request.urlopen(url).read().decode('utf-8')
        y = json.loads(data)
        if ( not len(y) ):
            self.send_reply( ("Map is not found!"), user, channel )
            return
        else:
            self.send_reply("Map (%s): %s by %s (%s) | http://resource.openra.net/%s/ | players: %s | type: %s | tileset: %s" % (y[0]['game_mod'], y[0]['title'], y[0]['author'], "x".join(y[0]['bounds'].split(',')[2:]), y[0]['id'], y[0]['players'], y[0]['map_type'], y[0]['tileset']), user, channel)
