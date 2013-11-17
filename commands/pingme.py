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
Ping you when 'someone' joins IRC: Usage: pingme when USERNAME join
"""

import re

def usage(self, user, channel):
    self.send_reply( ("Usage: "+self.command_prefix+"pingme when USERNAME join"), user, channel )

def pingme(self, user, channel):
    command = (self.command).split()
    if not re.search("^#", channel):
        message = "Command can be used only on a channel"
        self.send_notice( message, user )
        return
    conn, cur = self.db_data()
    if ( len(command) == 4 ):
        if ( command[1].lower() != 'when' ):
            usage(self, user, channel)
            cur.close()
            return
        if ( command[3].lower() != 'join' ):
            usage(self, user, channel)
            cur.close()
            return
        user_nicks = self.get_names(channel)
        user_join = command[2].lower()
        chars = ['`','-','_','[',']','{','}','\\','^']  # char which CAN be used in irc nick
        for i in range(len(user_join)):
            if ( (user_join[i] not in chars) and ( not re.search('[a-zA-Z0-9]', user_join[i])) ):
                self.send_reply( ("Username Error!"), user, channel)
                return
        if user_join in user_nicks:  # reciever is on the channel right now
            self.send_reply( ("User is online!"), user, channel)
            cur.close()
            return
        sql = """SELECT users_back FROM pingme
                WHERE who = '"""+user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):
            sql = """INSERT INTO pingme
                    (who,users_back)
                    VALUES
                    (
                    '"""+user+"""','"""+user_join+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
            self.send_reply( ("I will do it!"), user, channel )
        else:
            records_list = records[0][0].split(',')
            if ( user_join in records_list ):
                message = "You've already requested to ping you when "+user_join+" joins..."
                self.send_notice( message, user )
                return
            if ( len(records_list) == 20 ):
                message = "You've already requested `"+self.command_prefix+"pingme` of 20 users! I don't support more"
                self.send_notice( message, user )
                cur.close()
                return
            records_list.append(user_join)
            records_back = ",".join(records_list)
            sql = """UPDATE pingme
                    SET users_back = '"""+records_back+"""'
                    WHERE who = '"""+user+"""'
            """
            cur.execute(sql)
            conn.commit()
            self.send_reply( ("I will do it!"), user, channel )
    elif ( len(command) == 1 ):
        sql = """SELECT users_back FROM pingme
                WHERE who = '"""+user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):
            message = "You've not requested anything yet..."
            self.send_notice( message, user )
        else:
            message = "You will be pinged when next users join: " + records[0][0]
            self.send_notice( message, user )
    else:
        usage(self, user, channel)
    cur.close()
