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
Shows information of the last game generated
"""

import sqlite3

def lastgame(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) >= 1 ) and ( len(command) < 3 ):
        if ( len(command) == 1 ):
            sql = """SELECT team1,team2,type,host,map,time FROM pickup_game_start
                    ORDER BY uid DESC LIMIT 1
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            last_date = "-".join(row[5].split('-')[0:3])
            last_time = ":".join(row[5].split('-')[3:5])
            message = "@ "+row[2]+" || Time: "+last_date+" "+last_time+" GMT || Hoster: "+row[3]+" || Map: "+row[4]+" || Team 1: "+row[0]+" || Team 2: "+row[1]
            self.send_notice( message, user )
        else:
            modes = ['1v1','2v2','3v3','4v4','5v5']
            if command[1] in modes:
                mode = command[1]
                sql = """SELECT team1,team2,type,host,map,time FROM pickup_game_start
                    WHERE type = '"""+mode+"""'
                    ORDER BY uid DESC LIMIT 1
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if row != []:
                    last_date = "-".join(row[5].split('-')[0:3])
                    last_time = ":".join(row[5].split('-')[3:5])
                    message = "@ "+row[2]+" || Time: "+last_date+" "+last_time+" GMT || Hoster: "+row[3]+" || Map: "+row[4]+" || Team 1: "+row[0]+" || Team 2: "+row[1]
                    self.send_notice( message, user )
                else:
                    message = "No "+mode+" games played"
                    self.send_notice( message, user )
            else:
                self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                return
    else:
        self.send_message_to_channel( ("Error, wrong request"), channel )
    cur.close()
