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

# Module of JOIN event

def parse_event(self, recv):
    conn, cur = self.db_data()
    irc_join_nick = recv.split( '!' ) [ 0 ].split( ':' ) [ 1 ]
    irc_join_host = recv.split()[0].split('!')[1]
    chan = recv.split()[2].strip()
    if ( chan.startswith(':') ):
        chan = recv.split()[2][1:].strip()
    # logs
    self.logs(irc_join_nick, chan, 'join', irc_join_host, '')
    # last activity
    sql = """INSERT INTO activity
            (user,act,date_time,channel)
            VALUES
            (
            '"""+irc_join_nick.lower()+"""','join',strftime('%Y-%m-%d-%H-%M-%S'),'"""+chan+"""'
            )
    """
    cur.execute(sql)
    conn.commit()
    # for pingme
    sql = """SELECT who,users_back FROM pingme
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) != 0 ):
        for i in range(len(records)):
            who = records[i][0]
            users_back = records[i][1].split(',')
            if ( irc_join_nick.lower() in users_back ):
                self.send_reply( (irc_join_nick +' has joined IRC!'), who, who )
                records_index = users_back.index(irc_join_nick.lower())
                del users_back[records_index]
                users_back = ",".join(users_back)
                if ( len(users_back) == 0 ):
                    sql = """DELETE FROM pingme
                            WHERE who = '"""+who+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                else:
                    sql = """UPDATE pingme
                            SET users_back = '"""+users_back+"""'
                            WHERE who = '"""+who+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
    sql = """SELECT user FROM users
            WHERE user = '"""+irc_join_nick.lower()+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):   # user NOT found, add him
        sql = """INSERT INTO users
                (user,state)
                VALUES
                (
                '"""+irc_join_nick.lower()+"""',1
                )
        """
        cur.execute(sql)
        conn.commit()
        sql = """INSERT INTO user_channel
                (user, channel)
                VALUES
                (
                '"""+irc_join_nick.lower()+"""','"""+chan+"""'
                )
        """
        cur.execute(sql)
        conn.commit()
    else:   # user is in `users` table
        sql = """UPDATE users
                SET state = 1
                WHERE user = '"""+irc_join_nick.lower()+"""'
        """
        cur.execute(sql)
        conn.commit()
        sql = """SELECT status FROM user_channel
                WHERE user = '"""+irc_join_nick.lower()+"""' AND channel = '"""+chan+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):
            sql = """INSERT INTO user_channel
                    (user, channel)
                    VALUES
                    (
                    '"""+irc_join_nick.lower()+"""','"""+chan+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
        else:   # found record
            sql = """UPDATE user_channel
                    SET status = ''
                    WHERE user = '"""+irc_join_nick.lower()+"""' AND channel = '"""+chan+"""'
            """
            cur.execute(sql)
            conn.commit()
        sql = """SELECT sender,channel,date,message FROM later
                WHERE reciever = '"""+irc_join_nick.lower()+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):    # he has messages in database, read it
            messages_ = len(records) # number of messages for player
            self.send_message_to_channel( ("You have "+str(messages_)+" offline messages:"), irc_join_nick.lower() )
            for i in range(messages_):
                date_l = "-".join(records[i][2].split('-')[0:3])
                time_l = ":".join(records[i][2].split('-')[3:5])
                self.send_message_to_channel( ("### From: "+records[i][0]+";  channel: "+records[i][1]+";  date: "+date_l+" "+time_l), irc_join_nick.lower() )
                self.send_message_to_channel( (records[i][3]), irc_join_nick.lower() )
            sql = """DELETE FROM later
                    WHERE reciever = '"""+irc_join_nick.lower()+"""'
            """
            cur.execute(sql)
            conn.commit()
    cur.close()
