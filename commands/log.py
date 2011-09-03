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
import time
import re

def log(self, user, channel):
    if self.OpVoice(user, channel):
        command = (self.command)
        command = command.split()
        conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
        cur=conn.cursor()
        if ( len(command) == 1 ):
            if not re.search("^#", channel):
                sql = """SELECT * FROM commands
                        ORDER BY uid DESC LIMIT 10
                """
                cur.execute(sql)
                conn.commit()
                row = []
                logs = []
                actual = []
                for row in cur:
                    logs.append(row)
                for i in range(int(len(logs))):
                    actual.append(logs[i][1])
                    actual.append(logs[i][2])
                    actual.append(logs[i][3])
                    self.send_message_to_channel( ("User: "+actual[0]+"; Date: "+actual[2]+"; Command: ]"+actual[1]), user)
                    actual = []
                    time.sleep(0.5)
            else:
                self.send_message_to_channel( ("]log can't be used on a channel"), channel)
        cur.close()
    else:
        self.send_reply( ("Nice try!"), user, channel )
