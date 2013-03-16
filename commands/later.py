# Copyright 2011-2013 orabot Developers
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

import sqlite3

def later(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) >= 3 ):
        if ( channel.startswith('#') ):
            user_nick = command[1] # reciever
            if ( user_nick == user ):
                self.send_reply( (user+", you can not send a message to yourself"), user, channel)
            else:
                user_message = " ".join(command[2:])  # message
                user_nicks = self.get_names(channel)
                if user_nick in user_nicks:  # reciever is on the channel right now
                    self.send_reply( (user+", "+user_nick+" is on the channel right now!"), user, channel)
                else:   # reciever is not on the channel
                    # check if he exists in database
                    sql = """SELECT user FROM users
                            WHERE user = '"""+user_nick+"""'
                    
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    if ( len(records) == 0 ):
                        self.send_reply( ("Error! No such user in my database"), user, channel)
                    else:   # user exists
                        sql = """INSERT INTO later
                                (sender,reciever,channel,date,message)
                                VALUES
                                (
                                '"""+user+"""','"""+user_nick+"""','"""+channel+"""',strftime('%Y-%m-%d-%H-%M'),'"""+user_message+"""'
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_reply( ("The operation succeeded"), user, channel)
        else:
            self.send_message_to_channel( ("You can use ]later only on a channel"), user)
    else:
        self.send_reply( ("Usage: ]later nick message"), user, channel )
    cur.close()
