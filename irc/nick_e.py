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

# Module for NICK event

def parse_event(self, recv):
    original_nick = recv.split(':')[1].split('!')[0]
    new_nick = recv.split()[2].replace(':','').replace('\r\n','')
    conn, cur = self.db_data()
    sql = """SELECT channel,status FROM user_channel
            WHERE user = '"""+original_nick.lower()+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    transfer_channel = []
    transfer_status = []
    for i in range(len(records)):
        channel = records[i][0]
        status = records[i][1]
        if ( status == None ):
            status = ''
        transfer_channel.append(channel)
        transfer_status.append(status)
        self.logs(original_nick, channel, 'nick', new_nick, '')
    sql = """DELETE FROM user_channel
            WHERE user = '"""+original_nick.lower()+"""'
    """
    cur.execute(sql)
    conn.commit()
    # last activity
    sql = """INSERT INTO activity
            (user,act,date_time)
            VALUES
            (
            '"""+original_nick.lower()+"""','nick',strftime('%Y-%m-%d-%H-%M-%S')
            )
    """
    cur.execute(sql)
    conn.commit()
    sql = """UPDATE users
            SET state = 0, date = strftime('%Y-%m-%d-%H-%M-%S')
            WHERE user = '"""+original_nick.lower()+"""'
    """
    cur.execute(sql)
    conn.commit()
    sql = """SELECT user FROM users
            WHERE user = '"""+new_nick.lower()+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):
        sql = """INSERT INTO users
                (user,state)
                VALUES
                (
                '"""+new_nick.lower()+"""',1
                )
        """
        cur.execute(sql)
        conn.commit()
        for i in range(len(transfer_channel)):
            sql = """INSERT INTO user_channel
                    (user,channel,status)
                    VALUES
                    (
                    '"""+new_nick.lower()+"""','"""+transfer_channel[i]+"""','"""+transfer_status[i]+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
    else:
        sql = """UPDATE users
                SET state = 1
                WHERE user = '"""+new_nick.lower()+"""'
        """
        cur.execute(sql)
        conn.commit()
        for i in range(len(transfer_channel)):
            sql = """INSERT INTO user_channel
                    (user,channel,status)
                    VALUES
                    (
                    '"""+new_nick.lower()+"""','"""+transfer_channel[i]+"""','"""+transfer_status[i]+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
    # for pingme
    sql = """DELETE FROM pingme
            WHERE who = '"""+original_nick.lower()+"""'
    """
    cur.execute(sql)
    conn.commit()
    sql = """SELECT who,users_back FROM pingme
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) != 0 ):
        for i in range(len(records)):
            who = records[i][0]
            users_back = records[i][1].split(',')
            if ( new_nick.lower() in users_back ):
                self.send_reply( (new_nick +' has joined IRC!'), who, who )
                records_index = users_back.index(new_nick.lower())
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
    # later
    sql = """SELECT sender,channel,date,message FROM later
            WHERE reciever = '"""+new_nick.lower()+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) != 0 ):    # he has messages in database, read it
        messages_ = len(records) # number of messages for player
        self.send_message_to_channel( ("You have "+str(messages_)+" offline messages:"), new_nick.lower() )
        for i in range(messages_):
            date_l = "-".join(records[i][2].split('-')[0:3])
            time_l = ":".join(records[i][2].split('-')[3:5])
            self.send_message_to_channel( ("### From: "+records[i][0]+";  channel: "+records[i][1]+";  date: "+date_l+" "+time_l), new_nick.lower() )
            self.send_message_to_channel( (records[i][3]), new_nick.lower() )
        sql = """DELETE FROM later
                WHERE reciever = '"""+new_nick.lower()+"""'
        """
        cur.execute(sql)
        conn.commit()
    cur.close()
