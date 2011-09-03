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

def pickup_remove(self, user, channel):
    if self.OpVoice(user, channel):
        command = (self.command)
        command = command.split()
        conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
        cur=conn.cursor()
        if ( len(command) == 2 ):
            modes = ['1v1','2v2','3v3','4v4','5v5']
            temp_mode = ''
            for temp_mode in modes:
                sql = """SELECT name FROM pickup_"""+temp_mode+"""
                        WHERE name = '"""+command[1]+"""'
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if command[1] in row:
                    sql = """DELETE FROM pickup_"""+temp_mode+"""
                            WHERE name = '"""+command[1]+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    message = "You removed "+command[1]+" from :: "+temp_mode+" ::"
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                    cur.close()
                    return
            message = "Error, "+command[1]+" is not detected added to any game"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
        cur.close()
    else:
        self.send_reply( ("Nice try!"), user, channel )
