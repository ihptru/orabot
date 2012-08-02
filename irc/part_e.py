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

import sqlite3

def parse_event(self, recv):
    conn, cur = self.db_data()
    irc_part_nick = recv.split( "!" )[ 0 ].split( ":" ) [ 1 ]
    irc_part_host = recv.split()[0].split('!')[1]
    chan = recv.split()[2].strip()
    ###logs
    self.logs(irc_part_nick, chan, 'part', irc_part_host, '')
    ###
    sql = """SELECT user FROM user_channel
            WHERE channel <> '"""+chan+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0  ):
        state = '0'
    else:
        name_other_channels = []
        for i in range(len(records)):
            name_other_channels.append(records[i][0])
        if ( irc_part_nick not in name_other_channels ):
            state = '0'
        else:
            state = '1'
    sql = """UPDATE users
            SET date = strftime('%Y-%m-%d-%H-%M-%S'), state = """+state+"""
            WHERE user = '"""+irc_part_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    sql = """DELETE FROM user_channel
            WHERE user = '"""+irc_part_nick+"""' AND channel = '"""+chan+"""'
    """
    cur.execute(sql)
    conn.commit()
    ### last activity
    sql = """INSERT INTO activity
            (user,act,date_time,channel)
            VALUES
            (
            '"""+irc_part_nick+"""','part',strftime('%Y-%m-%d-%H-%M-%S'),'"""+chan+"""'
            )
    """
    cur.execute(sql)
    conn.commit()
    ###
    ### for ping me
    sql = """DELETE FROM pingme
            WHERE who = '"""+irc_part_nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    ### for ]pick
    modes = ['1v1','2v2','3v3','4v4','5v5']
    for diff_mode in modes:
        sql = """DELETE FROM pickup_"""+diff_mode+"""
                WHERE name = '"""+irc_part_nick+"""'
        """
        cur.execute(sql)
        conn.commit()
    ### for notify
    sql = """DELETE FROM notify
            WHERE user = '"""+irc_part_nick+"""' AND timeout <> 'f' AND timeout <> 'forever'
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
