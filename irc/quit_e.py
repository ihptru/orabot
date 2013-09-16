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

# Module for QUIT event

import sqlite3

def parse_event(self, recv):
    conn, cur = self.db_data()
    irc_quit_nick = recv.split( "!" )[ 0 ].split( ":" ) [ 1 ]
    irc_quit_host = recv.split()[0].split('!')[1]
    try:
        reason = ' ('+recv.split('QUIT :')[1]+')'
    except:
        reason = ''
    # last activity
    sql = """INSERT INTO activity
            (user,act,date_time)
            VALUES
            (
            '"""+irc_quit_nick+"""','quit',strftime('%Y-%m-%d-%H-%M-%S')
            )
    """
    cur.execute(sql)
    conn.commit()
    sql = """UPDATE users
            SET date = strftime('%Y-%m-%d-%H-%M-%S'), state = 0
            WHERE user = '"""+irc_quit_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    sql = """SELECT channel FROM user_channel
            WHERE user = '"""+irc_quit_nick+"""'
    """
    cur.execute(sql)    #in current system: if user quits, we know on what channels he is
    records = cur.fetchall()
    conn.commit()
    for i in range(len(records)):
        channel = records[i][0]
        self.logs(irc_quit_nick, channel, 'quit', irc_quit_host, reason)
    sql = """DELETE FROM user_channel
            WHERE user = '"""+irc_quit_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    # for pingme
    sql = """DELETE FROM pingme
            WHERE who = '"""+irc_quit_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    # for pickup
    modes = ['1v1', '2v2', '3v3', '4v4', '5v5', '6v6']
    for diff_mode in modes:
        sql = """DELETE FROM pickup_"""+diff_mode+"""
                WHERE name = '"""+irc_quit_nick+"""'
        """
        cur.execute(sql)
        conn.commit()
    cur.close()
