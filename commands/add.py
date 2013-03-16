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
Add yourself for a pickup game (add {1v1|2v2|3v3|4v4|5v5|6v6}
"""

import sqlite3
import re
from datetime import date
import random
import time
import subprocess
import os
import random

import config

def add(self, user, channel):        
    command = (self.command).split()
    conn, cur = self.db_data()
    if re.search("^#", channel):
        if ( len(command) > 1 ) and ( len(command) < 4 ):   #normal about of arguments
            modes = ['1v1','2v2','3v3','4v4','5v5','6v6']
            if ( command[1] not in modes ):
                self.send_reply( ("Invalid game mode! Try again"), user, channel )
                return
            else:
                amount_players_required = self.players_for_mode(command[1])
                # check complaints
                sql = """SELECT complaints FROM pickup_stats
                        WHERE name = '"""+user+"""'
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) != 0 ):
                    num_complaints = records[0][0]
                    if ( int(num_complaints) > 10 ):
                        self.send_reply( (user+", you have too many complaints, please contact more privileged user to figure out this issue"), user, channel )
                        return
                mode = command[1]
                sql = """SELECT name FROM pickup_"""+mode+"""
                        WHERE name = '"""+user+"""'
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) != 0 ):
                    self.send_reply( (user+" is already added for |"+mode+"| - Operation failed"), user, channel )
                    return
                modes.remove(mode)
                for diff_mode in modes:
                    sql = """SELECT name FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+user+"""'
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    if ( len(records) != 0 ):
                        self.send_reply( (user+" is already added for |"+diff_mode+"| - Operation failed"), user, channel )
                        return
                # timeout check
                sql = """SELECT name,timeout FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) != 0 ):   # players exist
                    current = time.mktime(time.strptime( time.strftime('%Y-%m-%d-%H-%M-%S'), '%Y-%m-%d-%H-%M-%S'))
                    for i in range(len(records)):
                        add_time = time.mktime(time.strptime( records[i][1], '%Y-%m-%d-%H-%M-%S'))
                        difference = current - add_time
                        if ( difference > 10800 ):    # some player was added more then 3 hours ago, remove him
                            sql = """DELETE FROM pickup_"""+mode+"""
                                    WHERE name = '"""+records[i][0]+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_reply( ("@ "+records[i][0]+" was removed. Reason: Timed Out (> 3 hours)"), user, channel )
                # generating match
                sql = """SELECT name FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                amount_players_left = int(amount_players_required) - len(records)
                if ( amount_players_left == 1 ):    # this player is last, generate match
                    sql = """INSERT INTO pickup_"""+mode+"""
                            (name,timeout)
                            VALUES
                            (
                            '"""+user+"""',strftime('%Y-%m-%d-%H-%M-%S')
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    self.send_reply( ("@ "+user+" is added for |"+mode+"|"), user, channel )
                    self.send_reply( ("@ Enough players for |"+mode+"|"), user, channel )
                    sql = """SELECT name FROM pickup_"""+mode+"""
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    name = []
                    for i in range(len(records)):
                        name.append(records[i][0])
                    team1 = []
                    team2 = []
                    while ( len(name) > amount_players_required/2  ):
                        temp_name = random.choice(name)
                        team1.append(temp_name)
                        name.remove(temp_name)
                    team2 = name
                    sql = """SELECT name,hash FROM pickup_maps
                             WHERE """+"\""+mode+"\""+""" = 1
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    map_name = []
                    map_hash = []
                    for i in range(len(records)):
                        map_name.append(records[i][0])
                        map_hash.append(records[i][1])
                    map_to_play = random.choice(map_name)
                    hash = map_hash[map_name.index(map_to_play)]
                    sql = """SELECT uid FROM pickup_game_start
                            ORDER BY uid DESC LIMIT 1
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    server_id = "1"
                    for i in range(len(records)):
                        server_id = str(int(records[i][0])+1)
                    message = "@ Server: pickupID "+server_id+" || "+mode+" || Map: "+map_to_play+" || Team 1: "+", ".join(team1)+" || Team 2: "+", ".join(team2)
                    self.send_reply( (message), user, channel )
                    team = team1+team2
                    for name in team:
                        self.send_message_to_channel( (message), name )
                        sql = """SELECT name FROM pickup_stats
                                WHERE name = '"""+name+"""'
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        if ( len(records) == 0 ):
                            sql = """INSERT INTO pickup_stats
                                    (name,games,complaints)
                                    VALUES
                                    (
                                    '"""+name+"""',1,0
                                    )
                            """
                            cur.execute(sql)
                            conn.commit()
                        else:
                            sql = """SELECT games FROM pickup_stats
                                    WHERE name = '"""+name+"""'
                            """
                            cur.execute(sql)
                            records = cur.fetchall()
                            conn.commit()
                            games = records[0][0]
                            games = str(int(games) + 1)
                            sql = """UPDATE pickup_stats
                                    SET games = """+games+"""
                                    WHERE name = '"""+name+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                    sql = """DELETE FROM pickup_"""+mode+"""
                    """
                    cur.execute(sql)
                    conn.commit()
                    sql = """INSERT INTO pickup_game_start
                            (team1,team2,type,map,maphash,time)
                            VALUES
                            (
                            '"""+", ".join(team1)+"""','"""+", ".join(team2)+"""','"""+mode+"""','"""+map_to_play+"""','"""+hash+"""',strftime('%Y-%m-%d-%H-%M-%S')
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    
                    ports = random.sample(range(0, 100), 100)
                    random_port = str(random.choice(ports))
                    port = "12"+random_port
                    if len(random_port) == 1:
                        port = port + "4"
                    os.chdir(config.openra_path)
                    subprocess.Popen(["mono", "OpenRA.Game.exe", "Game.Mods=ra", "Server.Map="+hash, "Server.Name=pickupID "+server_id+" | "+mode+" | do not enter if you are not supposed to play here", "Server.AdvertiseOnline=true", "Server.ListenPort="+port, "Server.ExternalPort="+port, "Server.Dedicated=true", "Server.DedicatedLoop=false", "Server.DedicatedMOTD=Team1: "+",\ ".join(team1)+" | Team2: "+", ".join(team2)+"  ||  If you are not in a team, you can spectate or substitute"])
                else:
                    sql = """INSERT INTO pickup_"""+mode+"""
                            (name,timeout)
                            VALUES
                            ('"""+user+"""',strftime('%Y-%m-%d-%H-%M-%S')
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    self.send_reply( ("@ "+user+" is added for |"+mode+"|"), user, channel )
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
    else:
        self.send_message_to_channel( ("`add` can be used only on a channel"), user )
    cur.close()
