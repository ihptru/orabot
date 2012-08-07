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
Shows information of the pickup last game generated
"""

import sqlite3

def lastgame(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) >= 1 ) and ( len(command) < 3 ):
        if ( len(command) == 1 ):
            sql = """SELECT team1,team2,type,map,time FROM pickup_game_start
                    ORDER BY uid DESC LIMIT 1
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( len(records) == 0 ):
                self.send_notice( 'No games played', user )
                return
            last_date = "-".join(records[0][5].split('-')[0:3])
            last_time = ":".join(records[0][5].split('-')[3:5])
            message = "@ Server: pickupID "+records[0][0]+" || "+records[0][3]+" || Time: "+last_date+" "+last_time+" GMT || Map: "+records[0][4]+" || Team 1: "+records[0][1]+" || Team 2: "+records[0][2]
            self.send_notice( message, user )
        else:
            modes = ['1v1','2v2','3v3','4v4','5v5', '6v6']
            if command[1] in modes:
                mode = command[1]
                sql = """SELECT uid,team1,team2,type,map,time FROM pickup_game_start
                    WHERE type = '"""+mode+"""'
                    ORDER BY uid DESC LIMIT 1
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( len(records) != 0 ):
                    last_date = "-".join(records[0][5].split('-')[0:3])
                    last_time = ":".join(records[0][5].split('-')[3:5])
                    message = "@ Server: pickupID "+records[0][0]+" || "+records[0][3]+" || Time: "+last_date+" "+last_time+" GMT || Map: "+records[0][4]+" || Team 1: "+records[0][1]+" || Team 2: "+records[0][2]
                    self.send_notice( message, user )
                else:
                    message = "No "+mode+" games played"
                    self.send_notice( message, user )
            else:
                self.send_reply( ("Invalid game mode! Try again"), user, channel )
                return
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()
