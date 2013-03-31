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

"""
Shows current games.\n
More info at  http://wiki.lv-vl.net/index.php/IRC_orabot
"""

import sqlite3
import re
import urllib.request
import time
import datetime
import json
import getopt

def get_country( self, ip ):
    return self.data_from_url("http://api.hostip.info/country.php?ip="+ip, None)

def modinfo( mod ):
    mod_split = mod.split('@')
    if ( len(mod_split) == 1 ):
        return (mod_split[0].upper()).ljust(23)
    else:
        version = "@".join(mod_split[1:])
        version_split = version.split('-')
        if ( len(version_split) == 1 ):
            result_version = version
        else:
            if ( version_split[0] in ['release','playtest'] ):
                result_version = version_split[0] + '-' + version_split[1][4:]
                if ( len(version_split) == 3):
                    result_version += "-" + version_split[2]
            else:
                result_version = version
        return (mod_split[0].upper().ljust(5)[0:4] + '@' + result_version).ljust(18)

def copyRequired(dictlist, key, valuelist):
    return [dictio for dictio in dictlist if dictio[key] in valuelist]

def updated(self, user, channel):
    last_updated = self.games_last_updated[0]
    current_time = time.mktime(time.strptime( time.strftime('%Y-%m-%d-%H-%M-%S'), '%Y-%m-%d-%H-%M-%S'))
    difference = current_time - last_updated
    if (difference > 600):
        diff_result = str(datetime.timedelta(seconds = difference))
        self.send_reply( ("== list was updated "+diff_result+" ago =="), user, channel)

def games(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    y = self.games[:]   # fresh copy of games
    updated(self, user, channel)
    if ( len(y) == 0 ):
        self.send_reply( ("No games found"), user, channel )
        return
    # read keys
    optlist,  args = getopt.getopt(command[1:], 'parvls', ['show-empty', 'mods=', 'version='])
    if len(args) != 0:
        self.send_notice( ("Your input is inaccurate... use ]help games"), user)
        return
    arguments = [opt[0] for opt in optlist]
    # imply filters
    if '--show-empty' not in arguments:
        y = copyRequired(y, 'players', [str(l) for l in range(1,21)])   # show servers only with people
    # process orders
    if len(arguments) == 0 or ( len(arguments) == 1 and '--show-empty' in arguments):
        y = copyRequired(y, 'state', '1')
        if len(y) == 0:
            self.send_reply( ("Nothing to output"), user, channel )
            return
        y = sorted(y, key=lambda k: int(k['players']))   # always sort by amount of players in result
        y.reverse()
        for game in y:
            country = get_country(self, " ".join(game['address'].rsplit(':',1)))
            sname = game['name']
            if ( len(sname) == 0 ):
                sname = 'noname'
            players = game['players']
            games = '@ '+sname.strip().ljust(15)[0:15]+' - '+players.ljust(3)[0:2]+' - '+modinfo(game['mods'])+' - '+country
            self.send_reply( (games), user, channel )
            time.sleep(0.2)
        self.send_reply( ("Use http://mailaender.name/openra/  instead"), user, channel )
        return

    self.send_notice( ("Your input is inaccurate... use ]help games"), user)
    cur.close()
