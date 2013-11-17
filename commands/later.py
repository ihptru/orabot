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
Command is used to send an offline message to irc user
"""

def later(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) >= 3 ):
        if ( channel.startswith('#') ):
            user_nicknames = command[1].split(',') # reciever (or recievers, if splitted by comma)
            user_nicks = self.get_names(channel)
            for user_nick in user_nicknames:
                if ( user_nick.lower() == user ):
                    self.send_reply( ("Error! You can't send a message to yourself"), user, channel)
                else:
                    user_message = " ".join(command[2:])  # message
                    if user_nick.lower() in user_nicks:  # reciever is on the channel right now
                        self.send_reply( ("Error! "+user_nick+" is online!"), user, channel)
                    else:   # reciever is not on the channel
                        # check if he exists in database
                        sql = """SELECT user FROM users
                                WHERE user = '"""+user_nick.lower()+"""'
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        if ( len(records) == 0 ):
                            self.send_reply( ("Error! Unknown nickname: '"+user_nick+"'"), user, channel)
                        else:   # user exists
                            sql = """INSERT INTO later
                                    (sender,reciever,channel,date,message)
                                    VALUES
                                    (
                                    '"""+user+"""','"""+user_nick.lower()+"""','"""+channel+"""',
                                    strftime('%Y-%m-%d-%H-%M'),'"""+user_message+"""'
                                    )
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_reply( ("The operation succeeded for " + user_nick), user, channel)
        else:
            self.send_message_to_channel( ("You can use ]later only on a channel"), user)
    else:
        self.send_reply( ("Usage: ]later nick[,nick1,...] message"), user, channel )
    cur.close()
