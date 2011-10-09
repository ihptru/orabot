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
import config

def parse_event(self, recv):
    original_nick = recv.split(':')[1].split('!')[0]
    new_nick = recv.split()[2].replace(':','').replace('\r\n','')
    conn = sqlite3.connect('../db/openra.sqlite')
    cur = conn.cursor()
    ### for logs
    sql = """SELECT channels FROM users
            WHERE user = '"""+original_nick+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):   #user not found in table users
        for chan in config.log_channels.split(','):
            self.logs(original_nick, chan, 'nick', new_nick, '')
    else:   #user found
        if ( records[0][0] == '' ) or ( records[0][0] == None ):  #no channels found; reason(probably bot was offline when user joined or user was added manually)
            for chan in config.log_channels.split(','):
                self.logs(original_nick, chan, 'nick', new_nick, '')
        else:   #there are channels
            db_channels = records[0][0].split(',')
            for chan in db_channels:
                self.logs(original_nick, chan, 'nick', new_nick, '')
    ###
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
                (user,state,channels)
                VALUES
                (
                '"""+new_nick+"""',1,'"""+chan+"""'
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
    cur.close()
