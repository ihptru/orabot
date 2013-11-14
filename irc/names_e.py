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

# Module for NAMES event

def parse_event(self, recv):
    channel = recv.split()[4]
    users = " ".join(recv.split()[5:])[1:]
    conn, cur = self.db_data()
    sql = """DELETE FROM user_channel
            WHERE channel = '"""+channel+"""'
    """
    cur.execute(sql)
    conn.commit()
    for user in users.split():
        if ( user[0] in ['@','%','+'] ):
            status = user[0]
            user = user[1:]
        else:
            status = ''
        sql = """SELECT user FROM users
                WHERE user = '"""+user.lower()+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):       # no user found
            sql = """INSERT INTO users
                    (user,state)
                    VALUES
                    (
                    '"""+user.lower()+"""',1
                    )
            """
            cur.execute(sql)
            conn.commit()
            sql = """INSERT INTO user_channel
                    (user, channel, status)
                    VALUES
                    (
                    '"""+user.lower()+"""','"""+channel+"""','"""+status+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
        else:
            sql = """UPDATE users
                    SET state = 1
                    WHERE user = '"""+user.lower()+"""'
            """
            cur.execute(sql)
            conn.commit()
            sql = """INSERT INTO user_channel
                    (user, channel, status)
                    VALUES
                    (
                    '"""+user.lower()+"""','"""+channel+"""','"""+status+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
    cur.close()
