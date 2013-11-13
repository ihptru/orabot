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
Shows current games.\n
More info at  http://wiki.ihptru.net/index.php/IRC_orabot
"""

import re
import urllib.request
import time
import json
import getopt

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

def copyRequiredRegex(dictlist, key, regexObject):
    return [dictio for dictio in dictlist if regexObject.search(dictio[key])]

def games(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    url = 'http://master.open-ra.org/list_json.php'
    data = urllib.request.urlopen(url).read().decode()  # ping master server and fetch data
    y = json.loads(data)    # json object (fresh copy of games)
    if ( len(y) == 0 ):
        self.send_reply( ("No games found"), user, channel )
        return
    # read keys
    optlist,  args = getopt.getopt(command[1:], 'sr', ['show-empty', 'mods=', 'version='])   # priority exists here
    arguments = [opt[0] for opt in optlist]
    # imply filters
    if '-r' not in arguments and '-s' not in arguments: #don't imply other filters if this 2 options are set
        if '--show-empty' not in arguments:
            y = copyRequired(y, 'players', [str(l) for l in range(1,31)])   # show servers only with people
        if '--mods' in arguments:
            pass
        if '--version' in arguments:
            pass
    # process orders
    if '-s' in arguments:
        waiting = len(copyRequired(y, 'state', ['1']))
        playing = len(copyRequired(y, 'state', ['2']))
        games = "@ Games: waiting ["+str(waiting)+"] | playing ["+str(playing)+"]"
        self.send_reply( (games), user, channel )
        return
    if '-r' in arguments:   # will search even among started games
        chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore
        regex = " ".join(args)
        if len(regex) == 0:
            self.send_reply( ("'-r' requires a regex"), user, channel )
            return
        for i in range(len(chars)):
            if chars[i] in regex:
                check = 'true'
                break
            else:
                check = 'false'
        if check == 'false':
            p = re.compile(regex, re.IGNORECASE)
            listio = copyRequiredRegex(y, 'name', p)
            if len(listio) > 3:
                rk = 3
            else:
                rk = len(listio)
            for z in range(0, rk):
                sname = listio[z]['name']
                if ( len(sname) == 0 ):
                    sname = 'noname'
                players = listio[z]['players']
                games = '@ '+sname.strip().ljust(18)[0:18]+' - '+players.ljust(3)[0:2]+' - '+modinfo(listio[z]['mods'])
                self.send_reply( (games), user, channel )
            if len(listio) > 3:
                self.send_reply( ("I can't give you more then 3 results, but in sum, "+str(len(listio))+" servers match your request."), user, channel )
        return
    y = copyRequired(y, 'state', '1')
    if len(y) == 0:
        self.send_reply( ("No games are waiting for players"), user, channel )
        return
    y = sorted(y, key=lambda k: int(k['players']))   # always sort by amount of players in result
    y.reverse()
    for game in y:
        sname = game['name']
        if ( len(sname) == 0 ):
            sname = 'noname'
        players = game['players']
        games = '@ '+sname.strip().ljust(18)[0:18]+' - '+players.ljust(3)[0:2]+' - '+modinfo(game['mods'])
        self.send_reply( (games), user, channel )
        time.sleep(0.2)
    cur.close()
