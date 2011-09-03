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

def unnotify(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if ( user in row ):
            sql = """DELETE FROM notify
                    WHERE user = '"""+user+"""'
            """
            cur.execute(sql)
            conn.commit()
            message = "You are unsubscribed from new games notification"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
        else:
            message = "You are not subscribed for new games notification"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
    else:
        message = "Error arguments"
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
        self.irc_sock.send (str_buff.encode())
    cur.close()
