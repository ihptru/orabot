# Copyright 2011-2014 orabot Developers
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

def promote(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) == 2 ):
        modes = ['1v1','2v2','3v3','4v4','5v5', '6v6']
        mode = command[1]
        if mode in modes:
            amount_players_required = self.players_for_mode( mode )
            sql = """SELECT name FROM pickup_"""+mode+"""
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( len(records) == 0 ):
                message = "Promote Error, no players added for "+mode
                self.send_notice( message, user )
            else:
                message = "Please add up for |"+mode+"|! "+ str(amount_players_required-int(len(records))) + " more people needed! (Type "+self.command_prefix+"add "+mode+")"
                self.send_reply( (message), user, channel )
        else:
            self.send_reply( ("Invalid game mode! Try again"), user, channel )
            return
    elif ( len(command) > 2 ):
        self.send_reply( ("Error, wrong request"), user, channel )
    else:
        message = "Specify mode type to promote! 1v1, 2v2, 3v3, 4v4, 5v5 or 6v6"
        self.send_notice( message, user )
    cur.close()
