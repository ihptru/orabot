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
Command is used to show 10 last commands sent to bot
"""

import sqlite3

def log(self, user, channel):
    if not self.Admin(user, channel):
        return
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) == 1 ):
        sql = """SELECT user,command,date_time FROM commands
                ORDER BY uid DESC LIMIT 10
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        for i in range(len(records)):
            message = "User: "+records[i][0]+"; Date: "+records[i][2]+"; Command: "+self.command_prefix+records[i][1]
            self.send_notice( message, user )
    cur.close()
