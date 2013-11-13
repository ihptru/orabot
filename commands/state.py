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
Admin only: check online/offline state of user for debug purposes
"""

def state(self, user, channel):
    if not self.Admin(user, channel):
        return
    command = (self.command).split()
    if ( len(command) == 2 ):
        username = command[1]
        conn, cur = self.db_data()
        sql = """SELECT state FROM users
                WHERE user = '"""+username+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        cur.close()
        if ( len(records) == 0 ):
            self.send_reply( ("No such user"), user, channel )
        else:
            if records[0][0] == 0:
                state = 'offline'
            elif records[0][0] == 1:
                state = 'online'
            self.send_reply( (username+" is "+state), user, channel )
    else:
        self.send_notice("error",user)
