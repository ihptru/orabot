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

import re
import sqlite3
import time

### Admin commands

def quit(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        str_buff = ( "QUIT %s \r\n" ) % (channel)
        self.irc_sock.send (str_buff.encode())
        self.irc_sock.close()
        self.is_connected = False
        self.should_reconnect = False
        
def log(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        if not re.search("^#", channel):
            sql = """SELECT * FROM commands
                    ORDER BY uid DESC LIMIT 10
            """
            cur.execute(sql)
            conn.commit()
            row = []
            logs = []
            actual = []
            for row in cur:
                logs.append(row)
            for i in range(int(len(logs))):
                actual.append(logs[i][1])
                actual.append(logs[i][2])
                actual.append(logs[i][3])
                self.send_message_to_channel( ("User: "+actual[0]+"; Date: "+actual[2]+"; Command: ]"+actual[1].replace("~qq~","'")), user)
                actual = []
                time.sleep(0.5)
        else:
            self.send_message_to_channel( ("]log can't be used on a channel"), channel)
    cur.close()
            
def adduser(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        nick = command[1]
        sql = """SELECT * FROM users
                ORDER BY uid DESC LIMIT 1
        """
        cur.execute(sql)
        conn.commit()
        for row in cur:
            pass
        uid_users=row[0]
        uid_users = uid_users + 1
        
        sql = """SELECT * FROM users
                WHERE user = '"""+nick+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if nick in row: #users exists in database already
            if re.search("^#", channel):
                self.send_message_to_channel( ("Error! User already exists"), channel)
            else:
                self.send_message_to_channel( ("Error! User already exists"), user)
        else:   
            sql = """INSERT INTO users
                (uid,user)
                VALUES
                (
                """+str(uid_users)+",'"+nick+"'"+"""
                )
            """
            cur.execute(sql)
            conn.commit()
            if re.search("^#", channel):
                self.send_message_to_channel( ("Confirmed"), channel)
            else:
                self.send_message_to_channel( ("Confirmed"), user)
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()

def join(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    if ( len(command) == 2 ):
        if ( (command[1])[0] == "#"):
            irc_channel = command[1]
        else:
            irc_channel = "#" + command[1]
        self.join_channel(irc_channel)
        
def part(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    if ( len(command) == 2 ):
        if ( (command[1])[0] == "#"):
            irc_channel = command[1]
        else:
            irc_channel = "#" + command[1]
        self.quit_channel(irc_channel)
        
def complain(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        name = command[1]
        sql = """SELECT name,complaints FROM pickup_stats
                WHERE name = '"""+name+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if name not in row:
            message = "No such a user"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
        else:
            complaints = row[1]
            complaints = str(int(complaints) + 1)
            sql = """UPDATE pickup_stats
                    SET complaints = """+complaints+"""
                    WHERE name = '"""+name+"""'
            """
            cur.execute(sql)
            conn.commit()
            message = "Amount of "+name+"'s complaints increased by 1"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()

def register(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        if ( owner == '1' ):
            if not re.search("^#", channel):    #owner commands only in private
                register_nick = command[1]
                sql = """SELECT * FROM register
                        WHERE user = '"""+register_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if register_nick in row:
                    self.send_message_to_channel( ("User "+register_nick+" already exists"), user)
                else:
                    sql = """SELECT * FROM register
                            ORDER BY uid DESC LIMIT 1                                       
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    uid_register = row[0]
                    uid_register = uid_register + 1
                    sql = """INSERT INTO register
                            (uid,user)
                            VALUES
                            (
                            """+str(uid_register)+",'"+register_nick+"'"+"""
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    self.send_message_to_channel( ("User "+register_nick+" added successfully, he can use ]register to set up a password"), user)
                    self.send_message_to_channel( ("You are allowed to register with orabot by Global Administrator over (in private to bot): ]register password"), register_nick)
    cur.close()

def unregister(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        if ( owner == '1' ):
            if not re.search("^#", channel):    #owner commands only in private
                unregister_nick = command[1]
                sql = """SELECT * FROM register
                        WHERE user = '"""+unregister_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if unregister_nick not in row:
                    self.send_message_to_channel( ("User "+unregister_nick+" does not exist"), user)
                else:
                    sql = """DELETE FROM register
                            WHERE user = '"""+unregister_nick+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    self.send_message_to_channel( ("User "+unregister_nick+" is unregistered successfully"), user)
    cur.close()

def pickup_remove(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        modes = ['1v1','2v2','3v3','4v4','5v5']
        temp_mode = ''
        for temp_mode in modes:
            sql = """SELECT name FROM pickup_"""+temp_mode+"""
                    WHERE name = '"""+command[1]+"""'
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            if command[1] in row:
                sql = """DELETE FROM pickup_"""+temp_mode+"""
                        WHERE name = '"""+command[1]+"""'
                """
                cur.execute(sql)
                conn.commit()
                message = "You removed "+command[1]+" from :: "+temp_mode+" ::"
                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                self.irc_sock.send (str_buff.encode())
                cur.close()
                return
        message = "Error, "+command[1]+" is not detected added to any game"
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
        self.irc_sock.send (str_buff.encode())
    cur.close()

def subscribed(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        sql = """SELECT user FROM notify
        """
        cur.execute(sql)
        conn.commit()
        row = []
        subscribed = []
        for row in cur:
            subscribed.append(row[0])
        if ( subscribed == [] ):
            if re.search("^#", channel):
                self.send_message_to_channel( ("No one is subscribed for notifications"), channel )
            else:
                self.send_message_to_channel( ("No one is subscribed for notifications"), user )
        else:
            subscribed = ", ".join(subscribed)
            if re.search("^#", channel):
                self.send_message_to_channel( ("Subscribed users: "+subscribed), channel )
            else:
                self.send_message_to_channel( ("Subscribed users: "+subscribed), user )
    elif ( len(command) == 2 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+command[1]+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if ( command[1] in row ):
            if re.search("^#", channel):
                self.send_message_to_channel( ("Yes, "+command[1]+" is subscribed for notifications"), channel )
            else:
                self.send_message_to_channel( ("Yes, "+command[1]+" is subscribed for notifications"), user )
        else:
            if re.search("^#", channel):
                self.send_message_to_channel( ("No, "+command[1]+" is not subscribed for notifications"), channel )
            else:
                self.send_message_to_channel( ("No, "+command[1]+" is not subscribed for notifications"), user )
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()
