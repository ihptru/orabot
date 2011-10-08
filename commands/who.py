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
The command shows current list of games with players added in Pickup Game
"""

import sqlite3

def who(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) >= 1 ) and ( len(command) < 3 ):
        modes = ['1v1','2v2','3v3','4v4','5v5']
        if ( len(command) == 1 ):
            temp_mode = ''
            names = []
            for temp_mode in modes:
                amount_players_required = self.players_for_mode( temp_mode )
                sql = """SELECT name,host FROM pickup_"""+temp_mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                name = []
                for row in cur:
                    if ( row[1] == 1 ):
                        name.append(row[0]+"[h]")
                    else:
                        name.append(row[0])
                if name != []:
                    names.append(temp_mode + " ["+str(len(name))+"/"+str(amount_players_required)+"]: " + ", ".join(name))
            if names == []:
                message = "No game going on!"
                self.send_notice( message, user )
            else:
                message = "All games: "+" || ".join(names)
                self.send_notice( message, user )
        else:
            if command[1] in modes:
                mode = command[1]
                amount_players_required = self.players_for_mode( mode )
                sql = """SELECT name,host FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                name = []
                for row in cur:
                    if ( row[1] == 1 ):
                        name.append(row[0]+"[h]")
                    else:
                        name.append(row[0])
                if name == []:
                    message = "No players detected for :: "+mode+" ::"
                    self.send_notice( message, user )
                else:
                    message = "@ " + mode + " ["+str(len(name))+"/"+str(amount_players_required)+"]: " + ", ".join(name)
                    self.send_notice( message, user )
            else:
                self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                return

    else:
        self.send_message_to_channel( ("Error, wrong request"), channel )
    cur.close()
