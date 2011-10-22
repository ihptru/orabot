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
    conn, cur = self.db_data()
    irc_quit_nick = recv.split( "!" )[ 0 ].split( ":" ) [ 1 ]
    supy_host = recv.split()[0].split('!')[1]
    
    self.quit_store.append(irc_quit_nick)
    
    ### last activity
    sql = """INSERT INTO activity
            (user,act,date_time)
            VALUES
            (
            '"""+irc_quit_nick+"""','quit',strftime('%Y-%m-%d-%H-%M-%S')
            )
    """
    cur.execute(sql)
    conn.commit()
    ###
    ### for ]last and logs
    sql = """SELECT channels FROM users
            WHERE user = '"""+irc_quit_nick+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0 ):   #user not found in table users
        for chan in config.log_channels.split(','):
            self.logs(irc_quit_nick, chan, 'quit', supy_host, '')
    else:   #user found
        if ( records[0][0] == '' ) or ( records[0][0] == None ):  #no channels found; reason(probably bot was offline when user joined or user was added manually)
            for chan in config.log_channels.split(','):
                self.logs(irc_quit_nick, chan, 'quit', supy_host, '')
        else:   #there are channels
            db_channels = records[0][0].split(',')
            for chan in db_channels:
                self.logs(irc_quit_nick, chan, 'quit', supy_host, '')
    sql = """UPDATE users
            SET date = strftime('%Y-%m-%d-%H-%M-%S'), state = 0, channels = ''
            WHERE user = '"""+irc_quit_nick+"'"+"""
    """
    cur.execute(sql)
    conn.commit()
    ### for ping me
    sql = """DELETE FROM pingme
            WHERE who = '"""+irc_quit_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    ### for ]pick
    modes = ['1v1','2v2','3v3','4v4','5v5']
    diff_mode = ''
    for diff_mode in modes:
        sql = """DELETE FROM pickup_"""+diff_mode+"""
                WHERE name = '"""+irc_quit_nick+"""'
        """
        cur.execute(sql)
        conn.commit()
    ### for notify
    sql = """DELETE FROM notify
            WHERE user = '"""+irc_quit_nick+"""' AND timeout <> 'f' AND timeout <> 'forever'
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
