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
Complain if user is not shown for a pickup game (after 'some' amount of complaints, user is not allowed to add again)
"""

import sqlite3

def complain(self, user, channel):
    if not self.OpVoice(user, channel):
        return
    command = (self.command)
    command = command.split()
    conn, cur = self.db_data()
    if ( len(command) == 2 ):
        name = command[1]
        sql = """SELECT name,complaints FROM pickup_stats
                WHERE name = '"""+name+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if name not in row:
            message = "No such a user"
            self.send_notice( message, user )
        else:
            complaints = row[1]
            complaints = str(int(complaints) + 1)
            sql = """UPDATE pickup_stats
                    SET complaints = """+complaints+"""
                    WHERE name = '"""+name+"""'
            """
            cur.execute(sql)
            conn.commit()
            message = "Amount of "+name+"'s complaints increased by 1"
            self.send_notice( message, user )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()
