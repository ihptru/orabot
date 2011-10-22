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
import config

def notify(self, user, channel):
    if config.notifications == False:
        message = "The bot is run without notifications support!"
        self.send_notice( message, user )
        return
    command = (self.command)
    command = command.split()
    conn, cur = self.db_data()
    if ( len(command) == 1 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if ( user in row ):
            message = "You are already subscribed for new games notification"
            self.send_notice( message, user )
        else:
            sql = """INSERT INTO notify
                    (user,date)
                    VALUES
                    (
                    '"""+user+"',"+"""strftime('%Y-%m-%d-%H-%M-%S')
                    )
            """
            cur.execute(sql)
            conn.commit()
            message = "You are subscribed for new games notification"
            self.send_notice( message, user )
    elif ( len(command) > 1 ):
        length = len(command)
        result_mod = "all"
        result_version = "all"
        result_timeout = "all"
        result_num = "any"
        mod_defined = 0
        version_defined = 0
        timeout_defined = 0
        num_defined = 0
        mods = ['ra','cnc','yf','all']
        timeouts = ['s','m','h','d']
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if ( user in row ):
            message = "You are already subscribed for new games notification"
            self.send_notice( message, user )
            cur.close()
            return
        else:
            for i in range(1,int(length)):
                argument = command[i].split('=')
                if ( len(argument) == 2 ):
                    if ( argument[0] == '-m' ):     #mod
                        if ( mod_defined == 0 ):
                            if ( argument[1].lower() in mods ):
                                mod_defined = 1
                                result_mod = argument[1]
                                sql = """SELECT user FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                if ( user in row ):
                                    sql = """UPDATE notify
                                            SET mod = '"""+argument[1]+"""'
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                else:
                                    sql = """INSERT INTO notify
                                            (user,date,mod)
                                            VALUES
                                            (
                                            '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),'"+argument[1]+"""'
                                            )
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                            else:
                                sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "Error! I don't know such game mod! Try again"
                                self.send_notice( message, user )
                                cur.close()
                                return 
                        else:
                            sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            message = "Error! You have already defined mod! Try again"
                            self.send_notice( message, user )
                            cur.close()
                            return
                    elif ( argument[0] == '-v' ):   #version
                        if ( version_defined == 0 ):
                            chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore
                            if ( argument[1] not in chars ):
                                version_defined = 1
                                result_version = "contains "+argument[1]
                                sql = """SELECT user FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                if ( user in row ):
                                    sql = """UPDATE notify
                                            SET version = '"""+argument[1]+"""'
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                else:
                                    sql = """INSERT INTO notify
                                            (user,date,version)
                                            VALUES
                                            (
                                            '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),'"+argument[1]+"""'
                                            )
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                            else:
                                sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "Error! Incorrect version!"
                                self.send_notice( message, user )
                                cur.close()
                                return
                        else:
                            sql = """DELETE FROM notify
                                    WHERE user = '"""+user+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            message = "Error! You have already defined version! Try again"
                            self.send_notice( message, user )
                            cur.close()
                            return
                    elif ( argument[0] == '-t' ):   #timeout
                        if ( timeout_defined == 0 ):
                            try:
                                if ( (argument[1] == 'forever') or (argument[1] == 'f') or (argument[1] == 'till_quit') or (argument[1] == 'all') or ( argument[1][-1] in timeouts and type(int(argument[1][0:-1])) is int ) ):
                                    timeout_defined = 1
                                    result_timeout = argument[1]
                                    sql = """SELECT user FROM notify
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    row = []
                                    for row in cur:
                                        pass
                                    if ( user in row ):
                                        sql = """UPDATE notify
                                                SET timeout = '"""+argument[1]+"""'
                                                WHERE user = '"""+user+"""'
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                    else:
                                        sql = """INSERT INTO notify
                                                (user,date,timeout)
                                                VALUES
                                                (
                                                '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),'"+argument[1]+"""'
                                                )
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                else:
                                    sql = """DELETE FROM notify
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    message = "Timeout Syntax Error! Try again"
                                    self.send_notice( message, user )
                                    cur.close()
                                    return
                            except:
                                sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "Timeout Syntax Error! Try again"
                                self.send_notice( message, user )
                                cur.close()
                                return
                        else:
                            sql = """DELETE FROM notify
                                    WHERE user = '"""+user+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            message = "Error! You have already defined timeout! Try again"
                            self.send_notice( message, user )
                            cur.close()
                            return
                    elif ( argument[0] == '-n' ):   #num players on server
                        if ( num_defined == 0 ):
                            try:
                                if ( (argument[1] == 'any') or type(int(argument[1][0:])) is int ):
                                    num_defined = 1
                                    result_num = argument[1]
                                    sql = """SELECT user FROM notify
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    row = []
                                    for row in cur:
                                        pass
                                    if ( user in row ):
                                        sql = """UPDATE notify
                                                SET num_players = '"""+argument[1]+"""'
                                                WHERE user = '"""+user+"""'
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                    else:
                                        sql = """INSERT INTO notify
                                                (user,date,num_players)
                                                VALUES
                                                (
                                                '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),'"+argument[1]+"""'
                                                )
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                else:
                                    sql = """DELETE FROM notify
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    message = "-n Syntax Error! Try again"
                                    self.send_notice( message, user )
                                    cur.close()
                                    return
                            except:
                                sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "-n Syntax Error! Try again"
                                self.send_notice( message, user )
                                cur.close()
                                return
                        else:
                            sql = """DELETE FROM notify
                                    WHERE user = '"""+user+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            message = "Error! You have already defined amount of players (-n)! Try again"
                            self.send_notice( message, user )
                            cur.close()
                            return
                    else:
                        sql = """DELETE FROM notify
                                WHERE user = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        message = "Syntax error!"+" What is "+argument[0]
                        self.send_notice( message, user )
                        cur.close()
                        return
                else:
                    sql = """DELETE FROM notify
                            WHERE user = '"""+user+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    message = "Syntax error!"
                    self.send_notice( message, user )
                    cur.close()
                    return
            message = "You are subscribed for new games notification; Mod: "+result_mod+"; Version: "+result_version+"; Minimum amount of players: "+result_num+"; Timeout: "+result_timeout
            self.send_notice( message, user )
    cur.close()
