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
Command is used to send an offline message to irc user
"""

import config
import re
import sqlite3

def later(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) >= 3 ):
        if re.search("^#", channel):
            user_nick = command[1].replace("'", "''") #reciever
            if ( user_nick == user ):
                self.send_message_to_channel( (user+", you can not send a message to yourself"), channel)
            else:
                user_message = " ".join(command[2:])  #message
                user_nicks = self.get_names(channel)
                if user_nick in user_nicks:  #reciever is on the channel right now
                    self.send_message_to_channel( (user+", "+user_nick+" is on the channel right now!"), channel)
                else:   #reciever is not on the channel
                    #check if he exists in database
                    sql = """SELECT user FROM users
                            WHERE user = '"""+user_nick+"'"+"""
                    
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = ''
                    for row in cur:
                        pass
                    if user_nick not in row:
                        self.send_message_to_channel( ("Error! No such user in my database"), channel)
                    else:   #user exists
                        sql = """INSERT INTO later
                                (sender,reciever,channel,date,message)
                                VALUES
                                (
                                '"""+user+"','"+user_nick+"','"+channel+"',strftime('%Y-%m-%d-%H-%M'),'"+user_message.replace("'","''")+"""'
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_message_to_channel( ("The operation succeeded"), channel)
        else:
            self.send_message_to_channel( ("You can use ]later only on a channel"), user)
    else:
        self.send_reply( ("Usage: ]later nick message"), user, channel )
    cur.close()
