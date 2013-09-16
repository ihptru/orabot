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

# No such Nick/Channel module: 401 event

import sqlite3

def parse_event(self, recv):
    nick = recv.split()[3]
    conn, cur = self.db_data()
    # for pingme
    sql = """DELETE FROM pingme
            WHERE who = '"""+nick+"""'
    """
    cur.execute(sql)
    conn.commit()
    # for pickup
    modes = ['1v1', '2v2', '3v3', '4v4', '5v5', '6v6']
    for diff_mode in modes:
        sql = """DELETE FROM pickup_"""+diff_mode+"""
                WHERE name = '"""+nick+"""'
        """
        cur.execute(sql)
        conn.commit()
    cur.close()
