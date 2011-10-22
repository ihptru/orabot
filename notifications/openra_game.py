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

import time
import config
import sqlite3
import re
import urllib.request

def start(self):
    notify_ip_list = []
    notify_players_list = []
    while True:
        time.sleep(15)
        parse_list(self, notify_ip_list, notify_players_list)
        
def parse_list(self, notify_ip_list, notify_players_list):
    ip_current_games = []
    players_current_games = []
    timeouts = ['s','m','h','d']
    flood_protection = 0
    url = 'http://master.open-ra.org/list.php'
    try:
        stream = self.data_from_url(url, None)
    except:
        return
    if ( stream != '' ):
        split_games = str(stream).split('\nGame')
        length_games = len(split_games)
        for i in range(int(length_games)):
            ip = split_games[i].split('\n\t')[3].split()[1].split(':')[0]

            ip_current_games.append(ip)

            state = split_games[i].split('\n\t')[4]
            players = split_games[i].split('\n\t')[5].split()[1]

            players_current_games.append(players)

            name = " ".join(split_games[i].split('\n\t')[2].split()[1:])
            mod = split_games[i].split('\n\t')[7].split()[1].split('@')[0]
            try:
                version = " - version: " + split_games[i].split('\n\t')[7].split()[1].split('@')[1]
            except:
                version = ''    #no version in output
            down = name.split('[down]')
            if ( ip in notify_ip_list ):
                if ( state == 'State: 2' ):
                    #game in list but started, remove from `notify_ip_list`
                    ip_index = notify_ip_list.index(ip)
                    del notify_ip_list[ip_index]
                    del notify_players_list[ip_index]
                    ip_index = ip_current_games.index(ip)
                    del ip_current_games[ip_index]
                    del players_current_games[ip_index]
                    conn = sqlite3.connect('db/openra.sqlite')
                    cur = conn.cursor()
                    sql = """INSERT INTO games
                            (game,players,date_time,version)
                            VALUES
                            (
                            '"""+name.replace("'","''")+"""','"""+players+"""',strftime('%Y-%m-%d-%H-%M-%S'),'"""+version+"""'
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    cur.close()
                elif ( state == 'State: 1' ):   #needed to check if amount of player is increased to number, users are subscribed for
                    ip_index_previous = notify_ip_list.index(ip)
                    ip_index_current = ip_current_games.index(ip)
                    if ( len(down) == 1 ):  #game is not [down]
                        conn = sqlite3.connect('db/openra.sqlite')
                        cur = conn.cursor()
                        sql = """SELECT user,date,mod,version,timeout,num_players FROM notify
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        data = []
                        for row in cur:
                            data.append(row)
                        if ( data != [] ):
                            length_data = len(data)
                            for i in range(int(length_data)):
                                flood_protection = flood_protection + 1
                                if flood_protection == 5:
                                    time.sleep(5)
                                    flood_protection = 0
                                db_user = data[i][0]
                                db_date = data[i][1]
                                db_mod = data[i][2]
                                db_version = data[i][3]
                                db_timeout = data[i][4]
                                db_num_players = data[i][5]
                                if ( db_mod.lower() == mod or db_mod.lower() == 'all' ):
                                    if ( re.search(db_version, version) or db_version.lower() == 'all' ):
                                        try:
                                            db_num_players = int(db_num_players)
                                            if db_num_players > int(notify_players_list[ip_index_previous]) and db_num_players <= int(players_current_games[ip_index_current]):
                                                check_num_players = True
                                            else:
                                                check_num_players = False
                                        except:
                                            check_num_players = False
                                        if ( check_num_players == True ):
                                            check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn)
                            flood_protection = 0
                        cur.close()
            else:   #ip is not in a list
                if ( state == 'State: 1' ):
                    notify_ip_list.append(ip)
                    notify_players_list.append(players)
                    if ( len(down) == 1 ):  #game is not [down]
                        conn = sqlite3.connect('db/openra.sqlite')
                        cur = conn.cursor()
                        sql = """SELECT user,date,mod,version,timeout,num_players FROM notify
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        data = []
                        for row in cur:
                            data.append(row)
                        if ( data != [] ):
                            length_data = len(data)
                            for i in range(int(length_data)):
                                flood_protection = flood_protection + 1
                                if flood_protection == 5:
                                    time.sleep(5)
                                    flood_protection = 0
                                db_user = data[i][0]
                                db_date = data[i][1]
                                db_mod = data[i][2]
                                db_version = data[i][3]
                                db_timeout = data[i][4]
                                db_num_players = data[i][5]
                                if ( db_mod.lower() == mod or db_mod.lower() == 'all' ):
                                    if ( re.search(db_version, version) or db_version.lower() == 'all' ):
                                        try:
                                            db_num_players = int(db_num_players)
                                            if db_num_players <= int(players):
                                                check_num_players = True
                                            else:
                                                check_num_players = False
                                        except:
                                            check_num_players = True
                                        if ( check_num_players == True ):
                                            check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn)
                            flood_protection = 0
                        cur.close()
        length = len(notify_ip_list)
        indexes = []
        for i in range(int(length)):
            if ( notify_ip_list[i] not in ip_current_games ):
                indexes.append(i)   #indexes to remove from notify_ip_list
            else:
                index_for_players = ip_current_games.index(notify_ip_list[i])
                notify_players_list[i] = players_current_games[index_for_players]
        for i in indexes:
            del notify_ip_list[i]
            del notify_players_list[i]

def check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn):
    notify_message = "New game: "+name+" - mod: "+mod+version+" - Already "+players+" players in"
    if ( db_timeout.lower() == 'all' ):
        self.send_reply( (notify_message), db_user, db_user )
    elif ( db_timeout.lower() == 'till_quit' ):
        self.send_reply( (notify_message), db_user, db_user )
    elif ( db_timeout.lower() == 'f' or db_timeout.lower() == 'forever' ):
        sql = """SELECT state FROM users
                WHERE user = '"""+db_user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):
            if ( str(records[0][0]) == '1' ):
                self.send_reply( (notify_message), db_user, db_user )
    else:
        date_of_adding_seconds = time.mktime(time.strptime( db_date, '%Y-%m-%d-%H-%M-%S'))
        localtime = time.strftime('%Y-%m-%d-%H-%M-%S')
        localtime = time.mktime(time.strptime( localtime, '%Y-%m-%d-%H-%M-%S'))
        difference = localtime - date_of_adding_seconds     #in result - must be less then timeout
        if ( db_timeout[-1] == 's' ):
            timeout = db_timeout[0:-1]
        elif ( db_timeout[-1] == 'm' ):
            timeout = int(db_timeout[0:-1]) * 60
        elif ( db_timeout[-1] == 'h' ):
            timeout = int(db_timeout[0:-1]) * 3600
        elif ( db_timeout[-1] == 'd' ):
            timeout = int(db_timeout[0:-1]) * 86400
        if ( difference < timeout ):
            self.send_reply( (notify_message), db_user, db_user )
        else:   # timeout is over
            sql = """DELETE from notify
                    WHERE user = '"""+db_user+"""'
            """
            cur.execute(sql)
            conn.commit()
