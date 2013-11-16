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

# Module of KICK event

def parse_event(self, recv):
    by = recv.split(':')[1].split('!')[0]
    whom = recv.split()[3]
    chan = recv.split()[2]
    reason = " ".join(recv.split()[4:]).replace(':','').replace('\r\n','')
    self.logs(whom, chan, 'kick', by, reason)
    conn, cur = self.db_data()
    sql = """SELECT user FROM user_channel
            WHERE channel <> '"""+chan+"""' AND user = '"""+whom.lower()+"""'
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) == 0  ):
        sql = """UPDATE users
                SET date = strftime('%Y-%m-%d-%H-%M-%S'), state = 0
                WHERE user = '"""+whom.lower()+"""'
        """
        cur.execute(sql)
        conn.commit()
    sql = """DELETE FROM user_channel
            WHERE user = '"""+whom.lower()+"""' AND channel = '"""+chan+"""'
    """
    cur.execute(sql)
    conn.commit()
    # last activity
    sql = """INSERT INTO activity
            (user,act,date_time,channel)
            VALUES
            (
            '"""+whom.lower()+"""','kick',strftime('%Y-%m-%d-%H-%M-%S'),'"""+chan+"""'
            )
    """
    cur.execute(sql)
    conn.commit()
    # for pingme
    sql = """DELETE FROM pingme
            WHERE who = '"""+whom.lower()+"""'
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
