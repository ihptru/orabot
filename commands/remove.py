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
Removes a user performing a command from any game he is added to... (user can specify an optional argument - mode)
"""

import sqlite3
import re

def remove(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if re.search("^#", channel):
        if ( len(command) >= 1 ) and ( len(command) < 3 ):
            modes = ['1v1','2v2','3v3','4v4','5v5']
            if ( len(command) == 1 ):
                for temp_mode in modes:
                    sql = """SELECT name FROM pickup_"""+temp_mode+"""
                            WHERE name = '"""+user+"""'
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    if ( len(records) != 0 ):
                        sql = """DELETE FROM pickup_"""+temp_mode+"""
                                WHERE name = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        message = "You are removed from :: "+temp_mode+" ::"
                        self.send_notice( message, user )
                        return
                message = "Error, you are not detected added to any game"
                self.send_notice( message, user )
            else:
                if command[1] in modes:
                    mode = command[1]
                    sql = """SELECT name FROM pickup_"""+mode+"""
                            WHERE name = '"""+user+"""'
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    if ( len(records) != 0 ):
                        sql = """DELETE FROM pickup_"""+mode+"""
                                WHERE name = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        message = "You are removed from :: "+mode+" ::"
                        self.send_notice( message, user )
                        return
                    message = "Error, you are not detected added to :: "+mode+" ::"
                    self.send_notice( message, user )
                else:
                    self.send_reply( ("Invalid game mode! Try again"), user, channel )
                    return
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
    else:
        self.send_message_to_channel( ("]remove can be used only on a channel"), user )
    cur.close()
