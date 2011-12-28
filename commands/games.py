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
Shows current games.\n
Options:\n
\t(-w)
\t(-p)
\t(--all | -wp)
\t(-s)
\t(-l)
\t(-r)
\t(-v)
\t(-vw | -wv)
\t(-vp | -pv)
"""

import pygeoip
import sqlite3
import re
import urllib.request
import time
import json

def get_map_info( sha ):
    url = "http://oramod.lv-vl.net/api/map_data.php?hash=%s" % sha
    data = urllib.request.urlopen(url).read().decode('utf-8')
    y = json.loads(data)
    if len(y):
        return (y[0]['title'], '/' + y[0]['players'])
    else:
        return ('unknown', '')

def modinfo( mod ):
    mod_split = mod.split('@')
    if ( len(mod_split) == 1 ):
        return (mod_split[0].upper()).ljust(20)
    else:
        version = "@".join(mod_split[1:])
        version_split = version.split('-')
        if ( len(version_split) == 1 ):
            result_version = version
        else:
            if ( version_split[0] in ['release','playtest'] ):
                result_version = version_split[0] + '-' + version_split[1][4:]
            else:
                result_version = version
        return (mod_split[0].upper() + '@' + result_version).ljust(16)

def games(self, user, channel):
    command = (self.command).split()
    url = 'http://master.open-ra.org/list_json.php'
    conn, cur = self.db_data()
    if ( len(command) == 1 ):
        content = urllib.request.urlopen(url).read().decode('utf-8')
        if ( len(content) == 0 ):
            self.send_reply( ("No games found"), user, channel )
            return
        y = json.loads(content)
        count='0'
        for game in y:
            if ( game['state'] == '1' ):
                count='1'   # lock - there are games in State: 1
                state = '(W)'
                ### for location
                ip = " ".join(game['address'].split(':')[0:-1])    # ip address
                gi = pygeoip.GeoIP('GeoIP.dat')
                country = gi.country_code_by_addr(ip).upper()   #got country name
                ###
                sname = game['name']
                if ( len(sname) == 0 ):
                    sname = 'noname'
                map_name, max_players = get_map_info(game['map'])
                players = game['players']
                games = '@ '+sname.strip().ljust(15)[0:15]+' - '+state+' - '+players+max_players+' - '+map_name+' - '+modinfo(game['mods'])+' - '+country
                time.sleep(0.5)
                self.send_reply( (games), user, channel )
        if ( count == "0" ):    #appeared no games in State: 1
            self.send_reply( ("No games waiting for players found"), user, channel )
    elif ( len(command) == 2 ):   # ]games with args
        content = urllib.request.urlopen(url).read().decode('utf-8')
        if ( len(content) == 0 ):
            self.send_reply( ("No games found"), user, channel )
            return
        y = json.loads(content)
        if ( command[1] == "-w" ):   #request games in State = 1
            count='0'
            for game in y:
                if ( game['state'] == '1' ):
                    count='1'   # lock - there are games in State: 1
                    state = '(W)'
                    ### for location
                    ip = " ".join(game['address'].split(':')[0:-1])    # ip address
                    gi = pygeoip.GeoIP('GeoIP.dat')
                    country = gi.country_code_by_addr(ip).upper()   #got country name
                    ###
                    sname = game['name']
                    if ( len(sname) == 0 ):
                        sname = 'noname'
                    map_name, max_players = get_map_info(game['map'])
                    players = game['players']
                    games = '@ '+sname.strip().ljust(15)[0:15]+' - '+state+' - '+players+max_players+' - '+map_name+' - '+modinfo(game['mods'])+' - '+country
                    time.sleep(0.5)
                    self.send_reply( (games), user, channel )
            if ( count == "0" ):
                self.send_reply( ("No games waiting for players found"), user, channel )
        elif ( command[1] == "-p" ):     # request games in State = 2
            count = '0'
            for game in y:
                if ( game['state'] == '2' ):
                    count='1'   # lock - there are games in State: 2
                    state = '(P)'
                    ### for location
                    ip = " ".join(game['address'].split(':')[0:-1])    # ip address
                    gi = pygeoip.GeoIP('GeoIP.dat')
                    country = gi.country_code_by_addr(ip).upper()   #got country name
                    ###
                    sname = game['name']
                    if ( len(sname) == 0 ):
                        sname = 'noname'
                    map_name, max_players = get_map_info(game['map'])
                    players = game['players']
                    games = '@ '+sname.strip().ljust(15)[0:15]+' - '+state+' - '+players+max_players+' - '+map_name+' - '+modinfo(game['mods'])+' - '+country
                    time.sleep(0.5)
                    self.send_reply( (games), user, channel )
            if ( count == "0" ):    #appeared no games in State: 2
                self.send_reply( ("No started games found"), user, channel )
        elif ( (command[1] == "--all") or (command[1] == "-wp") ): # request games in both states
            for game in y:
                if ( game['state'] == '1' ):
                    state = '(W)'
                elif ( game['state'] == '2' ):
                    state = '(P)'
                ### for location
                ip = " ".join(game['address'].split(':')[0:-1])    # ip address
                gi = pygeoip.GeoIP('GeoIP.dat')
                country = gi.country_code_by_addr(ip).upper()   #got country name
                ###
                sname = game['name']
                if ( len(sname) == 0 ):
                    sname = 'noname'
                map_name, max_players = get_map_info(game['map'])
                players = game['players']
                games = '@ '+sname.strip().ljust(15)[0:15]+' - '+state+' - '+players+max_players+' - '+modinfo(game['mods'])+' - '+country
                time.sleep(0.5)
                self.send_reply( (games), user, channel )
        elif ( (command[1]) == "-l" ):
            games_state1 = ''
            games_state2 = ''
            for game in y:
                if ( game['state'] == '1' ):
                    state = 'W'
                elif ( game['state'] == '2' ):
                    state = 'P'
                sname = game['name']
                if ( len(sname) == 0 ):
                    sname = 'noname'
                players = game['players']
                if ( state == 'W' ):
                    games_state1 = games_state1+'\t'+('['+players+']').ljust(5)+sname.strip()+' - '+modinfo(game['mods'])+'||'
                elif ( state == 'P' ):
                    games_state2 = games_state2+'\t'+('['+players+']').ljust(5)+sname.strip()+' - '+modinfo(game['mods'])+'||'
            split_games_state1 = games_state1.split('||')
            split_games_state2 = games_state2.split('||')
            if ( len(split_games_state2) > 1 ):
                self.send_reply( ('Playing:'), user, channel )
                for i in range(len(split_games_state2) - 1):
                    self.send_reply( (split_games_state2[i]), user, channel )
                    time.sleep(0.5)
            if ( len(split_games_state1) > 1 ):
                self.send_reply( ('Waiting:'), user, channel )
                for i in range(len(split_games_state1) - 1):
                    self.send_reply( (split_games_state1[i]), user, channel )
                    time.sleep(0.5)
        elif ( (command[1]) == "-s" ):
            waiting = 0
            playing = 0
            for game in y:
                if ( game['state'] == '1' ):
                    waiting = waiting + 1
                elif ( game['state'] == '2' ):
                    playing = playing + 1
            games = "@ Games: waiting ["+str(waiting)+"] | playing ["+str(playing)+"]"
            self.send_reply( (games), user, channel )
        elif ( (command[1]) == "-v" or (command[1]) == "-vp" or (command[1]) == "-vw" or (command[1]) == "-wv" or (command[1]) == "-pv"):
            games_state1 = []
            games_state2 = []
            for game in y:
                if ( game['state'] == '1' ):
                    state = 'W'
                elif ( game['state'] == '2' ):
                    state = 'P'
                sname = game['name']
                if not ( sname[0:6] == '[down]' ):
                    if ( state == 'W' ):
                        games_state1.append(modinfo(game['mods']))
                    elif ( state == 'P' ):
                        games_state2.append(modinfo(game['mods']))
            mod_state1_ready = []
            mod_state2_ready = []
            for mod in games_state1:
                if mod not in mod_state1_ready:
                    mod_state1_ready.append(mod)
            for mod in games_state2:
                if mod not in mod_state2_ready:
                    mod_state2_ready.append(mod)
            mod_1_len = len(mod_state1_ready)
            mod_2_len = len(mod_state2_ready)
            mod_1_count = [0]*mod_1_len
            mod_2_count = [0]*mod_2_len
            for mod in games_state1:
                position = mod_state1_ready.index(mod)
                mod_1_count[position] = mod_1_count[position] + 1
            for mod in games_state2:
                position = mod_state2_ready.index(mod)
                mod_2_count[position] = mod_2_count[position] + 1
            def send_games(self, user, channel, games_state1, games_state2, mod_state1_ready, mod_state2_ready, mod_1_count, mod_2_count):
                if ( len(games_state2) > 0 ):
                    self.send_reply( ('Playing:'), user, channel )
                    for i in range(len(mod_state2_ready)):
                        mod = mod_state2_ready[i]
                        count_games = str(mod_2_count[i])
                        if count_games[-1] == '1':
                            end = ''
                        else:
                            end = 's'
                        games = '\t' + mod + ' : ' + count_games + ' game'+end
                        self.send_reply( (games), user, channel )
                        time.sleep(0.5)
                elif ( games_state1 == [] and mod_state1_ready == ['0'] ):
                    self.send_reply( ('No started games found'), user, channel )
                if ( len(games_state1) > 0 ):
                    self.send_reply( ('Waiting:'), user, channel )
                    for i in range(len(mod_state1_ready)):
                        mod = mod_state1_ready[i]
                        count_games = str(mod_1_count[i])
                        if count_games[-1] == '1':
                            end = ''
                        else:
                            end = 's'
                        games = '\t' + mod + ' : ' + count_games + ' game'+end
                        self.send_reply( (games), user, channel )
                        time.sleep(0.5)
                elif ( games_state2 == [] and mod_state2_ready == ['0'] ):
                    self.send_reply( ('No games waiting for players found'), user, channel )
            if ( command[1] == '-vw' or command[1] == '-wv' ):
                send_games(self, user, channel, games_state1, [], mod_state1_ready, ['0'], mod_1_count, mod_2_count)
            elif ( command[1] == '-vp' or command[1] == '-pv' ):
                send_games(self, user, channel, [], games_state2, ['0'], mod_state2_ready, mod_1_count, mod_2_count)
            else:
                send_games(self, user, channel, games_state1, games_state2, mod_state1_ready, mod_state2_ready, mod_1_count, mod_2_count)
        elif ( (command[1]) == "-r" ):
            self.send_reply( ("A pattern required"), user, channel )
        else:
            self.send_reply( ("Incorrect option!"), user, channel )
    elif ( len(command) > 2 ):
        if ( command[1] == "-r" ):  #patter request
            content = urllib.request.urlopen(url).read().decode('utf-8')
            if ( len(content) == 0 ):
                self.send_reply( ("No games found"), user, channel )
                return
            y = json.loads(content)
            chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore
            request_pattern = " ".join(command[2:])
            for i in range(len(chars)):
                if chars[i] in request_pattern:
                    check = 'tru'
                    break
                else:
                    check = 'fals'
            if ( check == 'fals' ):     #requested pattern does not contain any of 'forbidden' chars
                p = re.compile(request_pattern, re.IGNORECASE)
                count='0'
                for game in y:
                    sname = game['name']
                    if p.search(sname):
                        count='1'   # lock
                        if ( game['state'] == '1' ):
                            state = '(W)'
                        elif ( game['state'] == '2' ):
                            state = '(P)'
                        ### for location
                        ip = " ".join(game['address'].split(':')[0:-1])    # ip address
                        gi = pygeoip.GeoIP('GeoIP.dat')
                        country = gi.country_code_by_addr(ip).upper()   #got country name
                        ###
                        if ( len(sname) == 0 ):
                            sname = 'noname'
                        map_name, max_players = get_map_info(game['map'])
                        players = game['players']
                        games = '@ '+sname.strip().ljust(15)+' - '+state+' - Players: '+players+max_players+' - Map: '+map_name+' - '+modinfo(game['mods'])+' - '+country
                        time.sleep(0.5)
                        self.send_reply( (games), user, channel )
                if ( count == "0" ):    #appeared no matches
                    self.send_reply( ("No matches"), user, channel )
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()
