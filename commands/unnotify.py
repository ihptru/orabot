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
Unsubscribe from notifications
"""

import sqlite3

def unnotify(self, user, channel):
    if self.notifications_support == False:
        message = "The bot is run without notifications support!"
        self.send_notice( message, user )
        return
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) == 1 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 1 ):
            sql = """DELETE FROM notify
                    WHERE user = '"""+user+"""'
            """
            cur.execute(sql)
            conn.commit()
            message = "The operation succeeded!"
            self.send_notice( message, user )
        else:
            message = "Fail: you were not subscribed!"
            self.send_notice( message, user )
    else:
        message = "Error arguments"
        self.send_notice( message, user )
    cur.close()
