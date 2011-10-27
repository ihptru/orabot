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
Admin only: NAMES for channel with user's statuses for debug purposes
"""

def names(self, user, channel):
    if not self.Admin(user, channel):
        return
    command = (self.command).split()
    if ( len(command) == 2 ):
        conn, cur = self.db_data()
        sql = """SELECT user,status FROM user_channel
                WHERE channel = '"""+command[1]+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        cur.close()
        if ( len(records) == 0 ):
            self.send_reply( ("Nothing found"), user, channel )
        else:
            string = ''
            amount_names = len(records)
            for i in range(amount_names):
                username = records[i][0]
                status = records[i][1]
                if status == None:
                    status = ''
                string = string + status+username + ", "
            self.send_reply( ("Names["+str(amount_names)+"]: " + string), user, channel )
    else:
        self.send_notice( "Argument required: channel", user )
