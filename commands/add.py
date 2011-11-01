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
Add yourself for a pickup game
"""

import sqlite3
import re
from datetime import date
import random
import time

def add(self, user, channel):        
    command = (self.command).split()
    conn, cur = self.db_data()
    if re.search("^#", channel):
        if ( len(command) > 1 ) and ( len(command) < 4 ):   #normal about of arguments
            modes = ['1v1','2v2','3v3','4v4','5v5']
            if ( command[1] not in modes ):
                self.send_reply( ("Invalid game mode! Try again"), user, channel )
                return
            else:
                host = '0'
                if ( len(command) == 3 ):
                    if ( command[2] == 'host' ):
                        host = '1'  #user can host a game
                    else:
                        self.send_reply( ("What is '"+command[2]+"'? Try again"), user, channel )
                        return

                amount_players_required = self.players_for_mode(command[1])

                #check complaints
                sql = """SELECT complaints FROM pickup_stats
                        WHERE name = '"""+user+"""'
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) != 0 ):
                    num_complaints = records[0][0]
                    if ( int(num_complaints) > 10 ):
                        self.send_reply( ("You have too many complaints, please contact more privileged user to figure out this issue"), user, channel )
                        return
                mode = command[1]
                sql = """SELECT name FROM pickup_"""+mode+"""
                        WHERE name = '"""+user+"""'
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) != 0 ):
                    self.send_reply( ("You are already added for :: "+mode+" :: - Operation failed"), user, channel )
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
                        self.send_reply( ("You are already added for :: "+diff_mode+" :: - Operation failed"), user, channel )
                        return
                ### timeout check
                sql = """SELECT name,timeout FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) != 0 ):   #players exist
                    current = time.mktime(time.strptime( time.strftime('%Y-%m-%d-%H-%M-%S'), '%Y-%m-%d-%H-%M-%S'))
                    for i in range(len(records)):
                        add_time = time.mktime(time.strptime( records[i][1], '%Y-%m-%d-%H-%M-%S'))
                        difference = current - add_time
                        if ( difference > 10800 ):    #some player was added more then 3 hours ago, remove him
                            sql = """DELETE FROM pickup_"""+mode+"""
                                    WHERE name = '"""+records[i][0]+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_reply( ("@ "+remove_user+" was removed. Reason: Time Out"), user, channel )
                #generating match
                sql = """SELECT name FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                amount_players_left = int(amount_players_required) - len(records)
                if ( amount_players_left == 1 ):    # this player is last, check hosts and generate match
                    if ( host == '1' ):
                        sql = """INSERT INTO pickup_"""+mode+"""
                                (name,host,timeout)
                                VALUES
                                (
                                '"""+user+"""',"""+host+""",strftime('%Y-%m-%d-%H-%M-%S')
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_reply( ("@ "+user+" is successfully added for :: "+mode+" ::"), user, channel )
                        self.send_reply( ("@ Enough player detected for :: "+mode+" ::"), user, channel )
                        sql = """SELECT name FROM pickup_"""+mode+"""
                                WHERE host = 1
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        random_host = []
                        for i in range(len(records)):
                            random_host.append(records[i][0])
                        hoster = random.choice(random_host)
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
                        sql = """SELECT name FROM pickup_maps
                                 WHERE """+"\""+mode+"\""+""" = 1
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        name = []
                        for i in range(len(records)):
                            name.append(records[i][0])
                        map_to_play = random.choice(name)
                        message = "@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(team1)+" || Team 2: "+", ".join(team2)
                        self.send_reply( (message), user, channel )
                        team = team1+team2
                        for name in team:
                            self.send_message_to_channel( (message), name )
                            if ( hoster == name ):
                                host = 1
                            else:
                                host = 0
                            sql = """SELECT name FROM pickup_stats
                                    WHERE name = '"""+name+"""'
                            """
                            cur.execute(sql)
                            records = cur.fetchall()
                            conn.commit()
                            if ( len(records) == 0 ):
                                sql = """INSERT INTO pickup_stats
                                        (name,games,hosts,complaints)
                                        VALUES
                                        (
                                        '"""+name+"""',1,"""+str(host)+""",0
                                        )
                                """
                                cur.execute(sql)
                                conn.commit()
                            else:
                                sql = """SELECT games,hosts FROM pickup_stats
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                records = cur.fetchall()
                                conn.commit()
                                games = records[0][0]
                                hosts = records[0][1]
                                games = str(int(games) + 1)
                                hosts = str(int(hosts) + int(host))
                                sql = """UPDATE pickup_stats
                                        SET games = """+games+""", hosts = """+hosts+"""
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                        sql = """DELETE FROM pickup_"""+mode+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                        sql = """INSERT INTO pickup_game_start
                                (team1,team2,type,host,map,time)
                                VALUES
                                (
                                '"""+", ".join(team1)+"""','"""+", ".join(team2)+"""','"""+mode+"""','"""+hoster+"""','"""+map_to_play+"""',strftime('%Y-%m-%d-%H-%M-%S')
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:
                        sql = """SELECT name FROM pickup_"""+mode+"""
                                WHERE host = 1
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        if ( len(records) == 0 ):
                            self.send_reply( ("@ No any players added, want to be hosters and you are last. You can play only if you can host. Try again"), user, channel )
                            return
                        sql = """INSERT INTO pickup_"""+mode+"""
                            (name,host,timeout)
                            VALUES
                            ('"""+user+"""',"""+host+""",strftime('%Y-%m-%d-%H-%M-%S')
                            )
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_reply( ("@ "+user+" is successfully added for :: "+mode+" ::"), user, channel )
                        self.send_reply( ("@ Enough player detected for :: "+mode+" ::"), user, channel )
                        sql = """SELECT name FROM pickup_"""+mode+"""
                                WHERE host = 1
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        random_host = []
                        for i in range(len(records)):
                            random_host.append(records[i][0])
                        hoster = random.choice(random_host)
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
                        sql = """SELECT name FROM pickup_maps
                                WHERE """+"\""+mode+"\""+""" = 1
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        name = []
                        for i in range(len(records)):
                            name.append(records[i][0])
                        map_to_play = random.choice(name)
                        message = "@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(team1)+" || Team 2: "+", ".join(team2)
                        self.send_reply( (message), user, channel )
                        team = team1+team2
                        for name in team:
                            self.send_message_to_channel( (message), name )
                            if ( hoster == name ):
                                host = 1
                            else:
                                host = 0
                            sql = """SELECT name FROM pickup_stats
                                    WHERE name = '"""+name+"""'
                            """
                            cur.execute(sql)
                            records = cur.fetchall()
                            conn.commit()
                            if ( len(records) == 0 ):
                                sql = """INSERT INTO pickup_stats
                                        (name,games,hosts,complaints)
                                        VALUES
                                        ('"""+name+"""',1,"""+str(host)+""",0
                                        )
                                """
                                cur.execute(sql)
                                conn.commit()
                            else:
                                sql = """SELECT games,hosts FROM pickup_stats
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                games = records[0][0]
                                hosts = records[0][1]
                                games = str(int(games) + 1)
                                hosts = str(int(hosts) + int(host))
                                sql = """UPDATE pickup_stats
                                        SET games = """+games+""", hosts = """+hosts+"""
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                        sql = """DELETE FROM pickup_"""+mode+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                        sql = """INSERT INTO pickup_game_start
                            (team1,team2,type,host,map,time)
                            VALUES
                            (
                            '"""+", ".join(team1)+"""','"""+", ".join(team2)+"""','"""+mode+"""','"""+hoster+"""','"""+map_to_play+"""',strftime('%Y-%m-%d-%H-%M-%S')
                            )
                        """
                        cur.execute(sql)
                        conn.commit()
                else:
                    sql = """INSERT INTO pickup_"""+mode+"""
                            (name,host,timeout)
                            VALUES
                            ('"""+user+"""',"""+host+""",strftime('%Y-%m-%d-%H-%M-%S')
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    self.send_reply( ("@ "+user+" is successfully added for :: "+mode+" ::"), user, channel )
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
    else:
        self.send_message_to_channel( ("]add can be used only on a channel"), user )
    cur.close()
