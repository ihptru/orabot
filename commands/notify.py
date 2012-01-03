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
Subscribe for a new game notifications
"""

import sqlite3
import getopt

def notify(self, user, channel):
    if self.notifications_support == False:
        message = "The bot is run without notifications support!"
        self.send_notice( message, user )
        return
    command = (self.command).split()
    try:
        optlist,  args = getopt.getopt(command[1:], 'm:n:t:v:')
    except getopt.GetoptError as err:
        message = "Fail: incorrect option!"
        self.send_notice( message, user )
        print (err)
        return
    if (len(args) != 0 ):
        message = "Fail: incorrect arguments!"
        self.send_notice( message, user )
        return
    conn, cur = self.db_data()
    if ( optlist == [] ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):
            message = "Fail: you are already subscribed!"
            self.send_notice( message, user )
            cur.close()
            return
        else:
            sql = """INSERT INTO notify
                    (user,date,mod,version,timeout,num_players)
                    VALUES
                    (
                    '"""+user+"""',strftime('%Y-%m-%d-%H-%M-%S','now','localtime'),'any','any','none','no limit'
                    )
            """
            cur.execute(sql)
            conn.commit()
            message = "You will be notified of new games!"
            self.send_notice( message, user )
            cur.close()
            return
    else:
        mod = "any"
        players = "no limit"
        timeout = "none"
        version = "any"
        
        mods = ['ra','cnc','yf','any']
        timeouts = ['s','m','h','d']
        chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore

        for  i in range(len(optlist)):
            if optlist[i][0] == "-m":
                mod = optlist[i][1].strip()
            if optlist[i][0] == "-n":
                players = optlist[i][1].strip()
            if optlist[i][0] == "-t":
                timeout = optlist[i][1].strip()
            if optlist[i][0] == "-v":
                version = optlist[i][1].strip()

        if ( mod.lower() not in mods ):
            message = "Fail: unknown mod!"
            self.send_notice( message, user )
            cur.close()
            return

        versionOK = True
        for i in range(len(version)):
            if ( version[i] in chars ):
                versionOK = False
        if ( versionOK == False ):
            message = "Fail: unsupported char in version!"
            self.send_notice( message, user )
            cur.close()
            return

        playersOK = True
        try:
            trash = int(players)
        except:
            playersOK = False
        if ( playersOK == False ):
            if players != "no limit":
                message = "Fail: players must be int!"
                self.send_notice( message, user )
                cur.close()
                return
        
        if not ( (timeout == 'forever') or (timeout == 'f') or (timeout == 'till_quit') or (timeout == 'none') or ( timeout[-1] in timeouts and type(int(timeout[0:-1])) is int ) ):
            message = "Fail: error in timeout!"
            self.send_notice( message, user )
            cur.close()
            return

        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):
            message = "Fail: you are already subscribed!"
            self.send_notice( message, user )
            cur.close()
            return
        else:
            sql = """INSERT INTO notify
                    (user,date,mod,version,timeout,num_players)
                    VALUES
                    (
                    '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S','now','localtime'),'"+mod+"""','"""+version+"""','"""+timeout+"""','"""+players+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
            if timeout == 'f':
                timeout = 'forever'
            message = "You are subscribed! {mod: "+mod+"} {version contains: "+version+"} {min players: "+players+"} {timeout: "+timeout+"}"
            self.send_notice( message, user )
            cur.close()
            return
