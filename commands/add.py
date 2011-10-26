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
                self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                return
            else:
                host = '0'
                if ( len(command) == 3 ):
                    if ( command[2] == 'host' ):
                        host = '1'  #user can host a game
                    else:
                        self.send_message_to_channel( ("What is '"+command[2]+"'? Try again"), channel )
                        return

                amount_players_required = self.players_for_mode(command[1])

                #check complaints
                sql = """SELECT name,complaints FROM pickup_stats
                        WHERE name = '"""+user+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if user in row:
                    num_complaints = row[1]
                    if ( int(num_complaints) > 10 ):
                        self.send_message_to_channel( ("You have too many complaints, please contact more privileged user to figure out this issue"), channel )
                        return
                mode = command[1]
                sql = """SELECT name FROM pickup_"""+mode+"""
                        WHERE name = '"""+user+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if user in row:
                    self.send_message_to_channel( ("You are already added for :: "+mode+" :: - Operation failed"), channel )
                    return
                modes.remove(mode)
                diff_mode = ''
                for diff_mode in modes:
                    sql = """SELECT name FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+user+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    if user in row:
                        self.send_message_to_channel( ("You are already added for :: "+diff_mode+" :: - Operation failed"), channel )
                        return
                ### timeout check
                sql = """SELECT name,timeout FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                data = []
                for row in cur:
                    data.append(row)
                if row != []:   #players exist
                    a = date.today()
                    a = str(a)
                    a = a.split('-')
                    year = a[0]
                    month = a[1]
                    day = a[2]
                    b = time.localtime()
                    b = str(b)
                    hours = b.split('tm_hour=')[1].split(',')[0]
                    minutes = b.split('tm_min=')[1].split(',')[0]
                    if len(hours) == 1:
                        hours = '0'+hours
                    else:
                        hours = hours
                    if len(minutes) == 1:
                        minutes = '0'+minutes
                    else:
                        minutes = minutes
                    localtime = year+month+day+hours+minutes
                    data_length = len(data)
                    for i in range(int(data_length)):
                        add_time = "".join(str(data[i][1]).split('-'))
                        remove_user = data[i][0]
                        difference = int(localtime) - int(add_time)
                        if ( difference > 180 ):    #some player was added more then 3 hours ago, remove him
                            sql = """DELETE FROM pickup_"""+mode+"""
                                    WHERE name = '"""+remove_user+"'"+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_message_to_channel( ("@ "+remove_user+" was removed. Reason: Time Out"), channel )
                #generating match
                sql = """SELECT name FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                data = []
                for row in cur:
                    data.append(row)
                data_length = len(data)
                amount_players_left = int(amount_players_required) - int(data_length)
                if ( amount_players_left == 1 ):    # this player is last, check hosts and generate match
                    if ( host == '1' ):
                        sql = """INSERT INTO pickup_"""+mode+"""
                                (name,host,timeout)
                                VALUES
                                ('"""+user+"',"+host+""",strftime('%Y-%m-%d-%H-%M')
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_message_to_channel( ("@ "+user+" is successfully added for :: "+mode+" ::"), channel )
                        self.send_message_to_channel( ("@ Enough player detected for :: "+mode+" ::"), channel )
                        sql = """SELECT name FROM pickup_"""+mode+"""
                                WHERE host = 1
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        random_host = []
                        for row in cur:
                            random_host.append(row[0])
                        hoster = random.choice(random_host)
                        sql = """SELECT name FROM pickup_"""+mode+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        name = []
                        for row in cur:
                            name.append(row[0])
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
                        conn.commit()
                        row = []
                        name = []
                        for row in cur:
                            name.append(row[0])
                        map_to_play = random.choice(name)
                        message = "@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(list(team1))+" || Team 2: "+", ".join(list(team2))
                        self.send_message_to_channel( (message), channel )
                        team = team1+team2
                        name = ''
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
                            conn.commit()
                            row = []
                            for row in cur:
                                pass
                            if name not in row:
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
                                row = []
                                for row in cur:
                                    pass
                                games = row[0]
                                hosts = row[1]
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
                                ('"""+", ".join(list(team1))+"','"+", ".join(list(team2))+"','"+mode+"','"+hoster+"','"+map_to_play+"',"+"""strftime('%Y-%m-%d-%H-%M')
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:
                        sql = """SELECT name FROM pickup_"""+mode+"""
                                WHERE host = 1
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        random_host = []
                        for row in cur:
                            random_host.append(row)
                        if ( len(random_host) != 0 ):   #there are hosters
                            sql = """INSERT INTO pickup_"""+mode+"""
                                (name,host,timeout)
                                VALUES
                                ('"""+user+"',"+host+""",strftime('%Y-%m-%d-%H-%M')
                                )
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_message_to_channel( ("@ "+user+" is successfully added for :: "+mode+" ::"), channel )
                            self.send_message_to_channel( ("@ Enough player detected for :: "+mode+" ::"), channel )
                            sql = """SELECT name FROM pickup_"""+mode+"""
                                    WHERE host = 1
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            random_host = []
                            for row in cur:
                                random_host.append(row[0])
                            hoster = random.choice(random_host)
                            sql = """SELECT name FROM pickup_"""+mode+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            name = []
                            for row in cur:
                                name.append(row[0])
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
                            conn.commit()
                            row = []
                            name = []
                            for row in cur:
                                name.append(row[0])
                            map_to_play = random.choice(name)
                            message = "@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(list(team1))+" || Team 2: "+", ".join(list(team2))
                            self.send_message_to_channel( (message), channel )
                            team = team1+team2
                            name = ''
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
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                if name not in row:
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
                                    row = []
                                    for row in cur:
                                        pass
                                    games = row[0]
                                    hosts = row[1]
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
                                ('"""+", ".join(list(team1))+"','"+", ".join(list(team2))+"','"+mode+"','"+hoster+"','"+map_to_play+"',"+"""strftime('%Y-%m-%d-%H-%M')
                                )
                            """
                            cur.execute(sql)
                            conn.commit()
                        else:
                            self.send_message_to_channel( ("@ No any players added, want to be hosters and you are last. You can play only if you can host. Try again"), channel )
                            return

                else:
                    sql = """INSERT INTO pickup_"""+mode+"""
                            (name,host,timeout)
                            VALUES
                            ('"""+user+"',"+host+""",strftime('%Y-%m-%d-%H-%M')
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    self.send_message_to_channel( ("@ "+user+" is successfully added for :: "+mode+" ::"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), channel )
    else:
        self.send_message_to_channel( ("]add can be used only on a channel"), user )
    cur.close()
