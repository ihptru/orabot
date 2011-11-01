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

"""
Add/List/Remove faq manuals
"""

import sqlite3

def faq(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) == 1 ):
        sql = """SELECT item FROM faq
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):
            self.send_reply( ("Currently there are no items available..."), user, channel )
        else:
            str_records = ''
            for rec in records:
                str_records = str_records + rec[0] + ", "
            result = "Items: " + str_records[0:-2]
            self.send_reply( (result), user, channel )
    elif ( len(command) == 2 ):
        if ( command[1] == "set" ):
            self.send_reply( ("Usage: "+self.command_prefix+"faq set new_item_name item_description"), user, channel )
        elif ( command[1] == "remove" ):
            self.send_reply( ("Usage: "+self.command_prefix+"faq remove item_name"), user, channel )
        else:
            item = command[1]
            sql = """SELECT desc FROM faq
                    WHERE item = '"""+item+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( len(records) == 0 ):
                self.send_reply( ("Item is not set"), user, channel )
            else:
                self.send_reply( (item+": "+records[0][0]), user, channel )
    elif ( len(command) == 3 ):
        if ( command[1] == "remove" ):
            if not self.Admin(user, channel):
                return
            item = command[2]
            sql = """SELECT item FROM faq
                    WHERE item = '"""+item+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( len(records) == 0 ):
                self.send_reply( (item + ": not found..."), user, channel )
            else:
                sql = """DELETE FROM faq
                        WHERE item = '"""+item+"""'
                """
                cur.execute(sql)
                conn.commit()
                self.send_reply( (item + ": removed"), user, channel )
        elif ( command[1] == "set" ):
            self.send_reply( ("Usage: "+self.command_prefix+"faq set new_item_name item_description"), user, channel )
        else:
            self.send_reply( ("Error!"), user, channel )
    elif ( len(command) >= 4 ):
        if ( command[1] == "remove" ):
            self.send_reply( ("Usage: "+self.command_prefix+"faq remove item_name"), user, channel )
        elif ( command[1] == "set" ):
            if not self.Admin(user, channel):
                return
            item = command[2]
            sql = """SELECT item FROM faq
                    WHERE item = '"""+item+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if not ( len(records) == 0 ):
                self.send_reply( ("Error! Item already exists!"), user, channel )
            else:
                desc = " ".join(command[3:])
                sql = """INSERT INTO faq
                        (item,whoset,desc)
                        VALUES
                        (
                        '"""+item+"""','"""+user+"""','"""+desc+"""'
                        )
                """
                cur.execute(sql)
                conn.commit()
                self.send_reply( ("Done"), user, channel )
        else:
            self.send_reply( ("Error!"), user, channel )
    cur.close()
