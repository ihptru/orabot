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
Shows online players per Mod
"""

import urllib.request
import json

def players(self, user, channel):
    command = (self.command).split()
    if ( not len(command) == 1 ):
        return
    url = 'http://master.open-ra.org/list_json.php'
    try:
        data = urllib.request.urlopen(url).read().decode()  # ping master server and fetch data
    except:
        self.send_reply("Failed to fetch data from master server", user, channel)
        return
    y = json.loads(data)    # json object (fresh copy of games)
    if ( len(y) == 0 ):
        self.send_reply( ("Nothing found"), user, channel )
        return
    w_ra, w_td, w_d2k, w_other, p_ra, p_td, p_d2k, p_other = (0 for i in range(8))
    for game in y:
    	try:
    		mod = game['mods'].split('@')[0].lower()
    		if mod == 'ra':
    			if game['state'] == '1':
    				w_ra += int(game['players'])
    			else:
    				p_ra += int(game['players'])
    		elif mod == 'cnc':
    			if game['state'] == '1':
    				w_td += int(game['players'])
    			else:
    				p_td += int(game['players'])
    		elif mod == 'd2k':
    			if game['state'] == '1':
    				w_d2k += int(game['players'])
    			else:
    				p_d2k += int(game['players'])
    		else:
    			if game['state'] == '1':
    				w_other += int(game['players'])
    			else:
    				p_other += int(game['players'])
    	except:
    		continue
    if_other = ""
    if w_other != 0:
    	if_other = "; Other: %s" % w_other
        if p_other != 0:
    	   if_other += " (%s)" % p_other
    else:
        if p_other != 0:
            if_other = "; Other: 0 (%s)" % p_other
    result = "Waiting (playing) -->  RA: %s (%s); TD: %s (%s); D2k: %s (%s)%s" % (w_ra,p_ra,w_td,p_td,w_d2k,p_d2k,if_other)
    self.send_reply( (result), user, channel )