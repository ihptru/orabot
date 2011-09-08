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

import sqlite3

def unsubscribe(self, user, channel):
    if not self.OpVoice(user, channel):
        return
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+command[1]+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if command[1] in row:
            sql = """DELETE FROM notify
                    WHERE user = '"""+command[1]+"""'
            """
            cur.execute(sql)
            conn.commit()
            self.send_reply( ("Successfully"), user, channel )
        else:
            self.send_reply( (command[1]+" is not subscribed for notifications"), user, channel )
    else:
        self.send_reply( ("I take only 1 argument as user's name"), user, channel )
    cur.close()
