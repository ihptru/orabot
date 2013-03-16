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

# Module of KICK event

def parse_event(self, recv):
    by = recv.split(':')[1].split('!')[0]
    whom = recv.split()[3]
    chan = recv.split()[2]
    reason = " ".join(recv.split()[4:]).replace(':','').replace('\r\n','')
    self.logs(whom, chan, 'kick', by, reason)
    conn, cur = self.db_data()
    sql = """UPDATE users
            SET date = strftime('%Y-%m-%d-%H-%M-%S'), state = 0
            WHERE user = '"""+whom+"""'
    """
    cur.execute(sql)
    conn.commit()
    sql = """DELETE FROM user_channel
            WHERE user = '"""+whom+"""' AND channel = '"""+chan+"""'
    """
    cur.execute(sql)
    conn.commit()
    # last activity
    sql = """INSERT INTO activity
            (user,act,date_time,channel)
            VALUES
            (
            '"""+whom+"""','kick',strftime('%Y-%m-%d-%H-%M-%S'),'"""+chan+"""'
            )
    """
    cur.execute(sql)
    conn.commit()
    # for pingme
    sql = """DELETE FROM pingme
            WHERE who = '"""+whom+"""'
    """
    cur.execute(sql)
    conn.commit()
    # for pickup
    modes = ['1v1', '2v2', '3v3', '4v4', '5v5', '6v6']
    for diff_mode in modes:
        sql = """DELETE FROM pickup_"""+diff_mode+"""
                WHERE name = '"""+whom+"""'
        """
        cur.execute(sql)
        conn.commit()
    # for notify
    sql = """DELETE FROM notify
            WHERE user = '"""+whom+"""' AND timeout <> 'f' AND timeout <> 'forever'
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
