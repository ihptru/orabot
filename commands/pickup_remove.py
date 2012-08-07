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
Removes a user specified in command as a argument from any game he is added to
"""

import sqlite3

def pickup_remove(self, user, channel):
    if not self.Admin(user, channel):
        return
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) == 2 ):
        modes = ['1v1','2v2','3v3','4v4','5v5', '6v6']
        for temp_mode in modes:
            sql = """SELECT name FROM pickup_"""+temp_mode+"""
                    WHERE name = '"""+command[1]+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( len(records) != 0 ):
                sql = """DELETE FROM pickup_"""+temp_mode+"""
                        WHERE name = '"""+command[1]+"""'
                """
                cur.execute(sql)
                conn.commit()
                message = "You removed "+command[1]+" from |"+temp_mode+"|"
                self.send_notice( message, user )
                cur.close()
                return
        message = "Error, "+command[1]+" is not detected added to any game"
        self.send_notice( message, user )
    cur.close()
