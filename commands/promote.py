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
Shows a message to promote a game with amount of players needed
"""

import sqlite3

def promote(self, user, channel):
    command = (self.command)
    command = command.split()
    conn, cur = self.db_data()
    if ( len(command) == 2 ):
        modes = ['1v1','2v2','3v3','4v4','5v5']
        mode = command[1]
        if mode in modes:
            amount_players_required = self.players_for_mode( mode )
            sql = """SELECT name FROM pickup_"""+mode+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            name = []
            for row in cur:
                name.append(row[0])
            if ( name == [] ):
                message = "Promote Error, no players added for "+mode
                self.send_notice( message, user )
            else:
                message = "Please add up for :: "+mode+" :: ! "+ str(amount_players_required-int(len(name))) + " more people needed! (Type ]add "+mode+"  or  ]add "+mode+" host  ,if you can host)"
                self.send_message_to_channel( (message), channel )
        else:
            self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
            return
    elif ( len(command) > 2 ):
        self.send_message_to_channel( ("Error, wrong request"), channel )
    else:
        message = "Specify mode type to promote! 1v1, 2v2, 3v3, 4v4 or 5v5"
        self.send_notice( message, user )
    cur.close()
