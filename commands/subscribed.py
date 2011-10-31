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
Shows all subscribed for notifications users or the subscription state of a specific user if to specify
"""

import sqlite3

def subscribed(self, user, channel):
    if not self.Admin(user, channel):
        return
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) == 1 ):
        sql = """SELECT user FROM notify
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        subscribed = []
        for i in range(len(records)):
            subscribed.append(records[i][0])
        if ( subscribed == [] ):
            self.send_reply( ("No one is subscribed for notifications"), user, channel )
        else:
            subscribed = ", ".join(subscribed)
            self.send_reply( ("Subscribed users: "+subscribed), user, channel )
    elif ( len(command) == 2 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+command[1]+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):
            self.send_reply( ("Yes, "+command[1]+" is subscribed for notifications"), user, channel )
        else:
            self.send_reply( ("No, "+command[1]+" is not subscribed for notifications"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()
