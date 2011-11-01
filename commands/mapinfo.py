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
Shows the full openra map's information
"""

import sqlite3

def mapinfo(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if ( len(command) == 1 ):
        self.send_reply( ("Part of map's name required!"), user, channel )
    else:
        if ( command[1] == '--random' ):
            if ( len(command) == 2 ):
                sql = """SELECT mod,title,description,author,type,titleset,players FROM maps
                        ORDER BY RANDOM() LIMIT 1
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if ( records[0][2] == '' ):
                    description = ''
                else:
                    description = " - Description: "+records[0][2]
                self.send_reply( ("Map name: "+records[0][1]+" - Mod: "+records[0][0]+description+" - Author: "+records[0][3]+" - Max Players: "+str(records[0][6])+" - Type: "+records[0][4]+" - Titleset: "+records[0][5]), user, channel )
            else:
                self.send_reply( ("Error, wrong request"), user, channel )
        else:
            mods = ['ra','cnc','yf']
            cond = command[1].split('=')
            if ( cond[0] == '--mod' ):
                if ( cond[1] != '' ):
                    mod = cond[1]
                    if ( mod not in mods ):
                        self.send_reply( ("I don't know such a mod!"), user, channel )
                        cur.close()
                        return
                    else:
                        map_pattern = " ".join(command[2:])
            else:
                map_pattern = " ".join(command[1:])
                mod = ''
            sql = """SELECT mod,title,description,author,type,titleset,players FROM maps
                    WHERE upper(title) LIKE upper('%"""+map_pattern+"""%') and upper(mod) LIKE upper('%"""+mod+"""%')
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( len(records) == 0 ):
                self.send_reply( ("Map is not found!"), user, channel )
                cur.close()
                return
            elif ( len(records) == 1 ):
                if ( records[0][2] == '' ):
                    description = ''
                else:
                    description = " - Description: "+records[0][2]
                self.send_reply( ("Map name: "+records[0][1]+" - Mod: "+records[0][0]+description+" - Author: "+records[0][3]+" - Max Players: "+str(records[0][6])+" - Type: "+records[0][4]+" - Titleset: "+records[0][5]), user, channel )
            else:
                self.send_reply( ("Too many matches!"), user, channel )
                cur.close()
                return
    cur.close()
