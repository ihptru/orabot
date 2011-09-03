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

import config

show_possible=['games', 'help', 'version', 'hi', 'randomteam', 'tr', 'lang', 'last', 'online', 'weather', 'lastgame', 'who', 'promote', 'maps', 'say','mapinfo','calc','faq']

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
                self.send_message_to_channel( ("User: "+actual[0]+"; Date: "+actual[2]+"; Command: ]"+actual[1]), user)
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
                WHERE user = '"""+nick+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if nick in row: #users exists in database already
            self.send_reply( ("Error! User already exists"), user, channel )
        else:   
            sql = """INSERT INTO users
                (user)
                VALUES
                (
                '"""+nick+"""'
                )
            """
            cur.execute(sql)
            conn.commit()
            self.send_reply( ("Confirmed"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
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
        self.send_reply( ("Error, wrong request"), user, channel )
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
                    sql = """INSERT INTO register
                            (user)
                            VALUES
                            (
                            '"""+register_nick+"""'
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
            self.send_reply( ("No one is subscribed for notifications"), user, channel )
        else:
            subscribed = ", ".join(subscribed)
            self.send_reply( ("Subscribed users: "+subscribed), user, channel )
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
            self.send_reply( ("Yes, "+command[1]+" is subscribed for notifications"), user, channel )
        else:
            self.send_reply( ("No, "+command[1]+" is not subscribed for notifications"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()

def unsubscribe(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+command[1]+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if command[1] in row:
            sql = """DELETE FROM notify
                    WHERE user = '"""+command[1]+"""'
            """
            cur.execute(sql)
            conn.commit()
            self.send_reply( ("Successfully"), user, channel )
        else:
            self.send_reply( (command[1]+" is not subscribed for notifications"), user, channel )
    else:
        self.send_reply( ("I take only 1 argument as user's name"), user, channel )
    cur.close()

def say(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    if ( len(command) > 1 ):
        self.send_reply( (" ".join(command[1:])), user, channel )

def show(self, user, channel, owner, authenticated):
    command = (self.command)
    command = command.split()
    if ( len(command) >= 4 ):
        if ( command[-2] == '|' ):
            to_user = command[-1]
            if (( to_user[0] == '#' ) or ( to_user[0] == ',' )):
                self.send_reply( ("Impossible to redirect output to channel!"), user, channel )
                return
            if re.search("^#", channel):
                #send NAMES channel to server
                str_buff = ( "NAMES %s \r\n" ) % (channel)
                self.irc_sock.send (str_buff.encode())
                #recover all nicks on channel
                recv = self.irc_sock.recv( 4096 )

                if str(recv).find ( "353 "+config.bot_nick+" =" ) != -1:
                    user_nicks = str(recv).split(':')[2].rstrip()
                    user_nicks = user_nicks.replace('+','').replace('@','')
                    user_nicks = user_nicks.split(' ')

                if ( to_user not in user_nicks ):  #reciever is NOT on the channel
                    self.send_message_to_channel( (user+", I can not send an output of this command to user which is not on the channel!"), channel)
                    return
            show_command = command[1:-2]
            show_command = " ".join(show_command)
            show_command = show_command.replace(']','')
            show_command = show_command.split()
            if ( show_command[0] in show_possible ):
                self.command = " ".join(show_command)
                eval (show_command[0])(self, to_user, to_user, '0', '1')
            else:
                self.send_reply( ("I can not show output of this command to user"), user, channel )
        else:
            self.send_reply( ("Syntax error"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
