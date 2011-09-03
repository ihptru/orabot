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

def adduser(self, user, channel):
    if self.OpVoice(user, channel):
        command = (self.command)
        command = command.split()
        conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
        cur=conn.cursor()
        if ( len(command) == 2 ):
            nick = command[1]

            sql = """SELECT * FROM users
                    WHERE user = '"""+nick+"'"+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            if nick in row: #users exists in database already
                self.send_reply( ("Error! User already exists"), user, channel )
            else:   
                sql = """INSERT INTO users
                    (user)
                    VALUES
                    (
                    '"""+nick+"""'
                    )
                """
                cur.execute(sql)
                conn.commit()
                self.send_reply( ("Confirmed"), user, channel )
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
        cur.close()
    else:
        self.send_reply( ("Nice try!"), user, channel )
