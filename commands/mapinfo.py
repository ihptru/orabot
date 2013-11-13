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
Shows the full openra map's information
"""

import json
import urllib.request

def mapinfo(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 1 ):
        self.send_reply( ("Part of map's name required!"), user, channel )
    else:
        map_pattern = "%20".join(command[1:])
        url = "http://content.open-ra.org/api/map_data.php?title=%s" % map_pattern
        data = urllib.request.urlopen(url).read().decode('utf-8')
        y = json.loads(data)
        if ( not len(y) ):
            self.send_reply( ("Map is not found!"), user, channel )
            return
        else:
            if ( y[0]['description'] == '' ):
                description = ''
            else:
                description = " - Description: "+y[0]['description']
            self.send_reply( ("Map name: "+y[0]['title']+" - Mod: "+y[0]['mod']+description+" - Author: "+y[0]['author']+" - Max Players: "+y[0]['players']+" - Type: "+y[0]['type']+" - Titleset: "+y[0]['tileset']+" - Width: "+y[0]['width']+" - Height: "+y[0]['height']), user, channel )
