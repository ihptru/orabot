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

def parse_event(self, recv):
    original_nick = recv.split(':')[1].split('!')[0]
    new_nick = recv.split()[2].replace(':','').replace('\r\n','')
    conn, cur = self.db_data()
    ### for logs
    sql = """SELECT channel,status FROM user_channel
            WHERE user = '"""+original_nick+"""'
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
            WHERE user = '"""+original_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    ### last activity
    sql = """INSERT INTO activity
            (user,act,date_time)
            VALUES
            (
            '"""+original_nick+"""','nick',strftime('%Y-%m-%d-%H-%M-%S')
            )
    """
    cur.execute(sql)
    conn.commit()
    ###
    sql = """UPDATE users
            SET state = 0, date = strftime('%Y-%m-%d-%H-%M-%S')
            WHERE user = '"""+original_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    sql = """SELECT user FROM users
            WHERE user = '"""+new_nick+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):
        sql = """INSERT INTO users
                (user,state)
                VALUES
                (
                '"""+new_nick+"""',1
                )
        """
        cur.execute(sql)
        conn.commit()
        for i in range(len(transfer_channel)):
            sql = """INSERT INTO user_channel
                    (user,channel,status)
                    VALUES
                    (
                    '"""+new_nick+"""','"""+transfer_channel[i]+"""','"""+transfer_status[i]+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
    else:
        sql = """UPDATE users
                SET state = 1
                WHERE user = '"""+new_nick+"""'
        """
        cur.execute(sql)
        conn.commit()
        for i in range(len(transfer_channel)):
            sql = """INSERT INTO user_channel
                    (user,channel,status)
                    VALUES
                    (
                    '"""+new_nick+"""','"""+transfer_channel[i]+"""','"""+transfer_status[i]+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
    ### for ping me
    sql = """DELETE FROM pingme
            WHERE who = '"""+original_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    ### for ]pick
    modes = ['1v1','2v2','3v3','4v4','5v5']
    for diff_mode in modes:
        sql = """DELETE FROM pickup_"""+diff_mode+"""
                WHERE name = '"""+original_nick+"""'
        """
        cur.execute(sql)
        conn.commit()
    ### for notify
    sql = """DELETE FROM notify
            WHERE user = '"""+original_nick+"""' AND timeout <> 'f' AND timeout <> 'forever'
    """
    cur.execute(sql)
    conn.commit()
    ## later
    sql = """SELECT reciever FROM later
            WHERE reciever = '"""+new_nick+"'"+"""
    """
    cur.execute(sql)
    conn.commit()

    row = []
    for row in cur:
        pass
    if new_nick in row:    #he has messages in database, read it
        sql = """SELECT * FROM later
                WHERE reciever = '"""+new_nick+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
        row = []
        msgs = []
        for row in cur:
            msgs.append(row)
        msgs_length = len(msgs) #number of messages for player
        self.send_message_to_channel( ("You have "+str(msgs_length)+" offline messages:"), new_nick )
        for i in range(int(msgs_length)):
            who_sent = msgs[i][1]
            on_channel = msgs[i][3]
            message_date = msgs[i][4]
            offline_message = msgs[i][5]
            self.send_message_to_channel( ("### From: "+who_sent+";  channel: "+on_channel+";  date: "+message_date), new_nick )
            self.send_message_to_channel( (offline_message), new_nick )
        time.sleep(0.1)
        sql = """DELETE FROM later
                WHERE reciever = '"""+new_nick+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
    cur.close()
