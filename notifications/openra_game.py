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
import sqlite3
import re
import json

def start(self):
    # IP_LIST contains  all waiting games ( ex: {ip: amount_of_players} )
    IP_LIST = {}
    conn, cur = self.db_data()
    sql = """DELETE FROM user_notified
    """
    cur.execute(sql)
    conn.commit()
    while True:
        time.sleep(15)
        IP_LIST = parse_list(self, IP_LIST,  conn,  cur)
    cur.close()
        
def parse_list(self, IP_LIST,  conn,  cur):
    # CURRENT_LIST contains all games ( ex: {ip: amount_of_players } )
    CURRENT_LIST = {}
    timeouts = ['s','m','h','d']
    url = 'http://master.open-ra.org/list_json.php'
    try:
        stream = self.data_from_url(url, None)
    except:
        return
    if ( stream == '' ):
        return

    # get JSON object
    y = json.loads(stream)

    # take one game from server list per iteration
    for i in range(len(y)):
        ip = y[i]['address'].split(':')[0]
        state = y[i]['state']
        players = y[i]['players']
        CURRENT_LIST[ip] = players

        name = y[i]['name']
        mod = y[i]['mods'].split('@')[0]
        try:
            version = y[i]['mods'].split('@')[1]
        except:
            version = ' '    #no version in output
        down = name.split('[down]')
        # ip of current checked game is in the list of waiting games already ( so it's know and not new )
        if ( ip in IP_LIST.keys() ):
            if ( state == '2' ):
                # game in IP_LIST but already started , remove from this list
                IP_LIST.pop(ip)
                # we do not need this game in list of CURRENT games either
                CURRENT_LIST.pop(ip)
                # remove record if exists from `user_notifed` db table
                sql = """DELETE FROM user_notified
                            WHERE ip = '"""+ip+"""'
                """
                cur.execute(sql)
                conn.commit()
                # next db code is needed for (last game) command to show lately started games
                sql = """INSERT INTO games
                        (game,players,date_time,version)
                        VALUES
                        (
                        '"""+name.replace("'","''")+"""','"""+players+"""',strftime('%Y-%m-%d-%H-%M-%S'),'"""+version+"""'
                        )
                """
                cur.execute(sql)
                conn.commit()
            # we know that game is in waiting list already so it's not new
            # but we also notify user if he requested to notify him only if a certain amount of players appeared on server
            elif ( state == '1' ):
                # amount of players from list of waiting games ( IP_LIST )
                # and amount of players form list of current games ( CURRENT_LIST)
                # maybe different so we check changes
                if ( len(down) > 1 ):  # game is [down]: we do not show [down] games
                    continue
                sql = """SELECT user,date,mod,version,timeout,num_players FROM notify
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) == 0 ):
                    continue
                for i in range(len(records)):
                    db_user = records[i][0]
                    db_date = records[i][1]
                    db_mod = records[i][2]
                    db_version = records[i][3]
                    db_timeout = records[i][4]
                    db_num_players = records[i][5]
                    # if user specified mod distinct from 'any', check if it matches mod of current checked game
                    if not ( db_mod.lower() == mod or db_mod.lower() == 'any' ):
                        continue
                    # version pattern found?
                    if not ( re.search(db_version, version) or db_version.lower() == 'any' ):
                        continue
                    try:
                        db_num_players = int(db_num_players)
                        # if requested min amount of players to be shown is more then amount of players of current game from previous check:
                        # waiting games ( IP_LIST ) and
                        # less or equal then amount of players in CURRENT_LIST of same game
                        # ex:
                        #       requestd min 3 players on server
                        #       last time there were 2 players on server
                        #       now server has 4 ppl which is already more then requested
                        #       == in that case: notify user ==
                        if db_num_players > int(IP_LIST[ip]) and db_num_players <= int(CURRENT_LIST[ip]):
                            check_cond = True
                        else:
                            check_cond = False
                    except:
                        #default
                        check_cond = False
                    if ( check_cond ):
                        sql = """SELECT user,ip FROM user_notified
                                WHERE user = '"""+db_user+"""' AND ip = '"""+ip+"""'
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        if ( len(records) == 0 ):
                            check_and_notify(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn)
                            sql = """INSERT INTO user_notified
                                    (user,ip)
                                    VALUES
                                    (
                                    '"""+db_user+"""','"""+ip+"""'
                                    )
                            """
                            cur.execute(sql)
                            conn.commit()
        # current checked game is not in a list of previous games ( IP_LIST )
        # if it's waiting game : it's a new game
        else:
            # if game is not in list of previous games - we only need to check waiting games - do not care about started at all now
            if ( state == '1' ):
                # totally new game
                # previous list of games gets new record for next iteration
                IP_LIST[ip] = players
                if ( len(down) > 1 ):  #game is [down]
                    continue
                sql = """SELECT user,date,mod,version,timeout,num_players FROM notify
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) == 0 ):
                    continue
                for i in range(len(records)):
                    db_user = records[i][0]
                    db_date = records[i][1]
                    db_mod = records[i][2]
                    db_version = records[i][3]
                    db_timeout = records[i][4]
                    db_num_players = records[i][5]
                    if not ( db_mod.lower() == mod or db_mod.lower() == 'any' ):
                        continue
                    if not ( re.search(db_version, version) or db_version.lower() == 'any' ):
                        continue
                    try:
                        db_num_players = int(db_num_players)
                        # if no exception happend yet, user requested specified amount of players to be on server to notify
                        # check if there are already more or equal players on server then user requested
                        # if it's still less, we will check again in next iteration in block of code above ( where ip is in IP_LIST already )
                        if db_num_players <= int(players):
                            check_cond = True
                        else:
                            check_cond = False
                    except:
                        #default
                        check_cond = True
                    if ( check_cond ):
                        check_and_notify(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn)
    keys = []
    for key in IP_LIST.keys():
        # if key aka IP is not in current list, it's already outdated: remove it to prepare IP_LIST for next check of master server
        if key not in CURRENT_LIST.keys():
            keys.append(key)
    for key in keys:
        IP_LIST.pop(key)
        sql = """DELETE FROM user_notified
                WHERE ip = '"""+key+"""'
        """
        cur.execute(sql)
        conn.commit()
    return IP_LIST

def check_and_notify(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn):
    if (players == '0'):
        players =''
    else:
        players = "{ Players:01,16 "+players+" }"
    if (version != ' '):
        version = " { "+version[:-4]+"00,10 "+version[-4:]+" } "
    notify_message = "New game:04,01 "+name+" {01,09 "+mod.upper()+" }"+version+players
    if ( db_timeout.lower() == 'none' ):
        self.send_reply( (notify_message), db_user, db_user )
    # till_quit is actually default
    elif ( db_timeout.lower() == 'till_quit' ):
        self.send_reply( (notify_message), db_user, db_user )
    # `f` or `forever` option means that user will be always notified when he is online unless he send (unnotify) command
    elif ( db_timeout.lower() == 'f' or db_timeout.lower() == 'forever' ):
        sql = """SELECT state FROM users
                WHERE user = '"""+db_user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):
            # we are sure that user is online now so we can notify him
            if ( str(records[0][0]) == '1' ):
                self.send_reply( (notify_message), db_user, db_user )
    # there is a timeout
    else:
        date_of_adding_seconds = time.mktime(time.strptime( db_date, '%Y-%m-%d-%H-%M-%S'))
        localtime = time.mktime(time.strptime( time.strftime('%Y-%m-%d-%H-%M-%S'), '%Y-%m-%d-%H-%M-%S'))
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
            sql = """DELETE FROM user_notified
                    WHERE user = '"""+db_user+"""'
            """
            cur.execute(sql)
            conn.commit()
