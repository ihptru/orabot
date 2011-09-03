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

import socket, sys, multiprocessing, time
import os
import re
from datetime import date
import sqlite3
import hashlib
import random
import pywapi
import urllib.request
import imp
import inspect

import db_process
import notify
import commands
import admin_commands
import config

###
if not os.path.exists('db/openra.sqlite'):
    db_process.start(config.root_admin, config.root_admin_password)
###

# Defining a class to run the server. One per connection. This class will do most of our work.
class IRC_Server:

    # The default constructor - declaring our global variables
    # channel should be rewritten to be a list, which then loops to connect, per channel.
    # This needs to support an alternate nick.
    def __init__(self, host, port, nick, channel , password =""):
        self.irc_host = host
        self.irc_port = port
        self.irc_nick = nick
        self.irc_channel = channel
        self.irc_sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.is_connected = False
        self.should_reconnect = False
        self.command = ""
        

    ## The destructor - Close socket.
    def __del__(self):
        self.irc_sock.close()

    # This is the bit that controls connection to a server & channel.
    # It should be rewritten to allow multiple channels in a single server.
    # This needs to have an "auto identify" as part of its script, or support a custom connect message.       
    def connect(self):
        self.should_reconnect = True
        try:
            self.irc_sock.connect ((self.irc_host, self.irc_port))
        except:
            print ("Error: Could not connect to IRC; Host: " + str(self.irc_host) + "Port: " + str(self.irc_port))
            exit(1) # We should make it recconect if it gets an error here
        print ("Connected to: " + str(self.irc_host) + ":" + str(self.irc_port))

        str_buff = ("NICK %s \r\n") % (self.irc_nick)
        self.irc_sock.send (str_buff.encode())
        print ("Setting bot nick to " + str(self.irc_nick) )

        str_buff = ("USER %s 8 * :X\r\n") % (self.irc_nick)
        self.irc_sock.send (str_buff.encode())
        print ("Setting User")
        # Insert Alternate nick code here.

        # Insert Auto-Identify code here.
        if config.nickserv == True:
            data = "identify "+config.nickserv_password
            self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % ('NickServ', data)).encode() )
        
        for i in range(int(len(self.irc_channel))):
            str_buff = ( "JOIN %s \r\n" ) % (self.irc_channel[i])
            self.irc_sock.send (str_buff.encode())
            print ("Joining channel " + self.irc_channel[i] )
        
        self.is_connected = True
        self.listen()
        
    def listen(self):
        while self.is_connected:
            recv = self.irc_sock.recv( 4096 )
            ### for logs
            a = date.today()
            a = str(a)
            a = a.split('-')
            year = a[0]
            month = a[1]
            day = a[2]
            b = time.localtime()
            b = str(b)
            hours = b.split('tm_hour=')[1].split(',')[0]
            minutes = b.split('tm_min=')[1].split(',')[0]
            seconds = b.split('tm_sec=')[1].split(',')[0]
            if len(hours) == 1:
                real_hours = '0'+hours
            else:
                real_hours = hours
            if len(minutes) == 1:
                real_minutes = '0'+minutes
            else:
                real_minutes = minutes
            if len(seconds) == 1:
                real_seconds = '0'+seconds
            else:
                real_seconds = seconds
            ### for logs end
            if str(recv).find ( "PING" ) != -1:
                self.irc_sock.send ( "PONG ".encode() + recv.split() [ 1 ] + "\r\n".encode() )             

            if str(recv).find ( " PRIVMSG " ) != -1:
                irc_user_nick = str(recv).split ( '!' ) [ 0 ] . split ( ":")[1]
                irc_user_host = str(recv).split ( '@' ) [ 1 ] . split ( ' ' ) [ 0 ]
                irc_user_message = self.data_to_message(str(recv))
                chan = (str(recv)).split()[2]  #channel ex: #openra
                ###logs
                if re.search('^.*01ACTION', irc_user_message) and re.search('01$', irc_user_message):
                    irc_user_message_me = irc_user_message.split('01ACTION ')[1][0:-4]
                    if chan in config.log_channels.split(','):
                        row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' * '+irc_user_nick+' '+irc_user_message_me+'\n'
                        chan_d = chan.replace('#','')
                        filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                        dir = os.path.dirname(filename)
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        file = open(filename,'a')
                        file.write(row)
                        file.close()
                else:
                    if chan in config.log_channels.split(','):
                        row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' <'+irc_user_nick+'> '+str(irc_user_message)+'\n'
                        chan_d = chan.replace('#','')
                        filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                        dir = os.path.dirname(filename)
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        file = open(filename,'a')
                        file.write(row)
                        file.close()
                ### logs end
                
                print ( irc_user_nick + ": " + irc_user_message)
                # "]" Indicated a command
                if ( str(irc_user_message) != '' ):
                    if ( str(irc_user_message[0]) == "]" ):
                        self.command = str(irc_user_message[1:])
                        # (str(recv)).split()[2] ) is simply the channel the command was heard on.
                        self.process_command(irc_user_nick, ( (str(recv)).split()[2] ))
### when message cotains link, show title
                if re.search('.*http.*://.*', str(irc_user_message)):
                    flood_protection = 0
                    matches = re.findall(r"http.?://[^\s]*", str(irc_user_message))
                    for http_link in matches:
                        flood_protection = flood_protection + 1
                        if flood_protection == 5:
                            time.sleep(6)
                            flood_protection = 0
                        link = http_link.split('://')[1]
                        pre = http_link.split('http')[1].split('//')[0]
                        link = 'http'+pre+'//'+link
                        if re.search('http.*youtube.com/watch.*', link):
                            if re.search("^#", chan):
                                link = link.split('&')[0]
                                try:
                                    site = urllib.request.urlopen(link)
                                    site = site.read()
                                    site = site.decode('utf-8')
                                    title = site.split('<title>')[1].split('</title>')[0].lstrip().split('- YouTube')[0].rstrip().replace('&amp;','&').replace('&#39;', '\'')
                                    if ( title != 'YouTube - Broadcast Yourself.' ):    #video exists
                                        self.send_message_to_channel( ("Youtube: "+str(title)), chan )
                                except:
                                    pass    #do not write title in private
                        else:
                            if re.search("^#", chan):
                                try:
                                    site = urllib.request.urlopen(link)
                                    site = site.read()
                                    site = site.decode('utf-8')
                                    title = site.split('<title>')[1].split('</title>')[0].rstrip().lstrip()
                                    self.send_message_to_channel( ("Title: "+title), chan )
                                except:
                                    pass    #do not write title in private
                    flood_protection = 0
                if re.search('.*\#[0-9]*.*', str(irc_user_message)):
                    flood_protection = 0
                    matches = re.findall(r"#[0-9]*", str(irc_user_message))
                    if re.search("^#", chan):
                        for bug_report in matches:
                            flood_protection = flood_protection + 1
                            if flood_protection == 5:
                                time.sleep(6)
                                flood_protection = 0
                            bug_or_feature_num = bug_report.split('#')[1]
                            url = 'http://bugs.open-ra.org/issues/'+bug_or_feature_num
                            try:
                                stream = urllib.request.urlopen(url).read()
                                stream = stream.decode('utf-8')
                                fetched = stream.split('<title>')[1].split('</title>')[0].split('OpenRA - ')[1].split(' - open-ra')[0]
                                self.send_message_to_channel( (fetched+" | "+url), chan )
                            except:
                                pass
                        flood_protection = 0
###

            if str(recv).find ( " JOIN " ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                irc_join_nick = str(recv).split( '!' ) [ 0 ].split( ':' ) [ 1 ]
                if ( len(irc_join_nick.split()) == 1 ):
                    irc_join_host = str(recv).split( '!' ) [ 1 ].split( ' ' ) [ 0 ]
                    supy_host = str(recv).split()[0][3:]
                    chan = str(recv).split()[2].replace(':','')[0:-5].rstrip()
                    sql = """SELECT * FROM users
                            WHERE user = '"""+irc_join_nick+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    if irc_join_nick not in row:     #user NOT found, add him (if user is not in db, he could not have ]later message)
                        sql = """INSERT INTO users
                                (user,state)
                                VALUES
                                (
                                '"""+str(irc_join_nick)+"""',1
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:   #user is in `users` table; he can have ]later messages
                        #for ]last
                        sql = """UPDATE users
                                SET state = 1
                                WHERE user = '"""+str(irc_join_nick)+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        sql = """SELECT reciever FROM later
                                WHERE reciever = '"""+irc_join_nick+"'"+"""
                        """
                        cur.execute(sql)
                        conn.commit()

                        row = []
                        for row in cur:
                            pass
                        if irc_join_nick in row:    #he has messages in database, read it
                            sql = """SELECT * FROM later
                                    WHERE reciever = '"""+irc_join_nick+"'"+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            msgs = []
                            for row in cur:
                                msgs.append(row)
                            msgs_length = len(msgs) #number of messages for player
                            self.send_message_to_channel( ("You have "+str(msgs_length)+" offline messages:"), irc_join_nick )
                            for i in range(int(msgs_length)):
                                who_sent = msgs[i][1]
                                on_channel = msgs[i][3]
                                message_date = msgs[i][4]
                                offline_message = msgs[i][5]
                                self.send_message_to_channel( ("### From: "+who_sent+";  channel: "+on_channel+";  date: "+message_date), irc_join_nick )
                                self.send_message_to_channel( (offline_message), irc_join_nick )
                            time.sleep(0.1)
                            sql = """DELETE FROM later
                                    WHERE reciever = '"""+irc_join_nick+"'"+"""
                        
                            """
                            cur.execute(sql)
                            conn.commit()
                    ###logs
                    if chan in config.log_channels.split(','):
                        row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' '+'*** '+irc_join_nick+' <'+supy_host+'> has joined '+chan+'\n'
                        chan_d = chan.replace('#','')
                        filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                        dir = os.path.dirname(filename)
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        file = open(filename,'a')
                        file.write(row)
                        file.close()
                    ###
                cur.close()
                
            if str(recv).find ( " QUIT " ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                irc_quit_nick = str(recv).split( "!" )[ 0 ].split( ":" ) [ 1 ]
                supy_host = str(recv).split()[0][3:]
                #change authenticated status
                sql = """SELECT * FROM register
                        WHERE user = '"""+irc_quit_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if irc_quit_nick in row:
                    authenticated = row[4]
                    if authenticated == 1:
                        sql = """UPDATE register
                                SET authenticated = 0
                                WHERE user = '"""+irc_quit_nick+"'"+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                ### for ]last              
                sql = """UPDATE users
                        SET date = strftime('%Y-%m-%d-%H-%M-%S'), state = 0
                        WHERE user = '"""+str(irc_quit_nick)+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                cur.close()
                ### for ]pick
                modes = ['1v1','2v2','3v3','4v4','5v5']
                diff_mode = ''
                for diff_mode in modes:
                    sql = """DELETE FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+irc_quit_nick+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                ### for notify
                sql = """DELETE FROM notify
                        WHERE user = '"""+irc_quit_nick+"""'
                """
                cur.execute(sql)
                conn.commit()
                ##logs
                for chan in config.log_channels.split(','):
                    row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' '+'*** '+irc_quit_nick+' <'+supy_host+'> has quit IRC\n'
                    chan_d = chan.replace('#','')
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
            if str(recv).find ( " PART " ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                irc_part_nick = str(recv).split( "!" )[ 0 ].split( ":" ) [ 1 ]
                supy_host = str(recv).split()[0][3:]
                chan = str(recv)[0:-5].split()[2].rstrip()
                ###logout
                sql = """SELECT * FROM register
                        WHERE user = '"""+irc_part_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if irc_part_nick in row:
                    authenticated = row[4]
                    if authenticated == 1:
                        sql = """UPDATE register
                                SET authenticated = 0
                                WHERE user = '"""+irc_part_nick+"'"+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                ### for ]last              
                sql = """UPDATE users
                        SET date = strftime('%Y-%m-%d-%H-%M-%S'), state = 0
                        WHERE user = '"""+str(irc_part_nick)+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                cur.close()
                ### for ]pick
                modes = ['1v1','2v2','3v3','4v4','5v5']
                diff_mode = ''
                for diff_mode in modes:
                    sql = """DELETE FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+irc_part_nick+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                ### for notify
                sql = """DELETE FROM notify
                        WHERE user = '"""+irc_part_nick+"""'
                """
                cur.execute(sql)
                conn.commit()
                ###logs
                if chan in config.log_channels.split(','):
                    row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' '+'*** '+irc_part_nick+' <'+supy_host+'> has left '+chan+'\n'
                    chan_d = chan.replace('#','')
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                ###
                
            if str(recv).find ( " NICK " ) != -1:
                original_nick = str(recv).split(':')[1].split('!')[0]
                new_nick = str(recv).split()[2].replace(':','')[0:-5]
                for chan in config.log_channels.split(','):
                    row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' '+'*** '+original_nick+' is now known as '+new_nick+'\n'
                    chan_d = chan.replace('#','')
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
            
            if str(recv).find ( " TOPIC " ) != -1:
                nick = str(recv).split(':')[1].split('!')[0]
                topic = " ".join(str(recv).split()[3:]).replace(':','')[0:-5]
                chan = str(recv).split()[2]
                if chan in config.log_channels.split(','):
                    row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' '+'*** '+nick+' changes topic to "'+topic+'"\n'
                    chan_d = chan.replace('#','')
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                
                
            if str(recv).find ( " KICK " ) != -1:
                by = str(recv).split(':')[1].split('!')[0]
                whom = str(recv).split()[3]
                chan = str(recv).split()[2]
                reason = " ".join(str(recv).split()[4:]).replace(':','')[0:-5]
                if chan in config.log_channels.split(','):
                    row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' '+'*** '+whom+' was kicked by '+by+' ('+reason+')\n'
                    chan_d = chan.replace('#','')
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                
        if self.should_reconnect:
            self.connect()

    def data_to_message(self,data):
        data = data[data.find(':')+1:len(data)]
        data = " ".join(data.split()[3:])[1:-5].rstrip()
        return data

    # helper to remove some insanity.
    def send_reply(self,data,user,channel):
        target = channel if channel.startswith('#') else user
        self.send_message_to_channel(data,target)

    # This function sends a message to a channel, which must start with a #.
    def send_message_to_channel(self,data,channel):
        print ( ( "%s: %s") % (self.irc_nick, data) )
        self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % (channel, data)).encode() )
        
        ### for logs
        a = date.today()
        a = str(a)
        a = a.split('-')
        year = a[0]
        month = a[1]
        day = a[2]
        b = time.localtime()
        b = str(b)
        hours = b.split('tm_hour=')[1].split(',')[0]
        minutes = b.split('tm_min=')[1].split(',')[0]
        seconds = b.split('tm_sec=')[1].split(',')[0]
        if len(hours) == 1:
            real_hours = '0'+hours
        else:
            real_hours = hours
        if len(minutes) == 1:
            real_minutes = '0'+minutes
        else:
            real_minutes = minutes
        if len(seconds) == 1:
            real_seconds = '0'+seconds
        else:
            real_seconds = seconds
        if channel in config.log_channels.split(','):
            row = year+'-'+month+'-'+day+'T'+real_hours+':'+real_minutes+':'+real_seconds+' <'+self.irc_nick+'> '+str(data)+'\n'
            chan_d = str(channel).replace('#','')
            filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
            dir = os.path.dirname(filename)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file = open(filename,'a')
            file.write(row)
            file.close()
        ### for logs end

    # This function takes a channel, which must start with a #.
    def join_channel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "JOIN %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())
            # This needs to test if the channel is full

    # This function takes a channel, which must start with a #.
    def quit_channel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "PART %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())
            # This needs to modify the list of active channels
    
    # This function is for pickup matches code
    def players_for_mode(self, mode):
        return sum( map( int, mode.split('v') ) )
    
    def OpVoice(self, user, channel):
        #send NAMES channel to server
        str_buff = ( "NAMES %s \r\n" ) % (channel)
        self.irc_sock.send (str_buff.encode())
        #recover all nicks on channel
        recv = self.irc_sock.recv( 4096 )

        if str(recv).find ( "353 "+config.bot_nick+" =" ) != -1:
            user_nicks = str(recv).split(':')[2].rstrip()
            if '+'+user in user_nicks.split() or '@'+user in user_nicks.split():
                return True
            else:
                return False
    
    
    def evalAdminCommand(self, commandname, user, channel, owner, authenticated):
        imp.reload(admin_commands)
        command_function=getattr(admin_commands, commandname, None)
        if command_function != None:
            if inspect.isfunction(command_function):
                command_function(self, user, channel, owner, authenticated)
            
    def evalCommand(self, commandname, user, channel):
        imp.reload(commands)    
        command_function=getattr(commands, commandname, None)
        if command_function != None:
            if inspect.isfunction(command_function):
                command_function(self, user, channel)
            
    def process_command(self, user, channel):
        # This line makes sure an actual command was sent, not a plain "!"
        if ( len(self.command.split()) == 0):
            error = "Usage: ]command [arguments]"
            self.send_reply( (error), user, channel )
            return
        # So the command isn't case sensitive
        command = (self.command)
        # Break the command into pieces, so we can interpret it with arguments
        command = command.split()
        string_command = " ".join(command)

### START OF SPAM FILTER
        conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
        cur=conn.cursor()
        sql = """SELECT * FROM black_list
            WHERE user = '"""+user+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
        
        row = []
        for row in cur:
            pass
        check_ignore = '0'
        if user in row:
            ignore_count = row[3]
            ignore_minutes = str(ignore_count)+'0'
            ignore_date = "".join(str(row[2]).split('-'))
            a = date.today()
            a = str(a)
            a = a.split('-')
            year = a[0]
            month = a[1]
            day = a[2]
            b = time.localtime()
            b = str(b)
            hours = b.split('tm_hour=')[1].split(',')[0]
            minutes = b.split('tm_min=')[1].split(',')[0]
            if len(hours) == 1:
                hours = '0'+hours
            else:
                hours = hours
            if len(minutes) == 1:
                minutes = '0'+minutes
            else:
                minutes = minutes
            localtime = year+month+day+hours+minutes
            difference = int(localtime) - int(ignore_date)  #how many minutes after last ignore
            if int(difference) < int(ignore_minutes):
                check_ignore = '1'  #lock, start ignore
            else:   #no need to ignore, ignore_minutes < difference
                check_ignore = '0'
        if check_ignore == '0':
            sql = """SELECT uid FROM commands
                    ORDER BY uid DESC LIMIT 1
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            uid_commands = row[0]
            #clear 'commands' table after each 1 000 record
            if int(uid_commands) >= 1000:
                sql = """DELETE FROM commands WHERE uid > 30"""
                cur.execute(sql)
                conn.commit()
    
            #write each command into 'commands' table 
            sql = """INSERT INTO commands
                    (user,command,date_time)
                    VALUES
                    (
                    '"""+str(user)+"','"+string_command.replace("'","''")+"',"+"strftime('%Y-%m-%d-%H-%M-%S')"+""" 
                    )        
            """
            cur.execute(sql)
            conn.commit()
            
            #extract last 30 records
            sql = """SELECT * FROM commands
                ORDER BY uid DESC LIMIT 30
            """
            cur.execute(sql)

            var=[]
            for row in cur:
                var.append(row)
            var.reverse()
            actual=[]
            user_data=[]
            for i in range(30):
                if user in str(var[i][1]):
                    actual.append(str(var[i][1]))   #name
                    actual.append(str(var[i][3]))   #date and time
                    user_data.append(actual)
                    actual=[]
            user_data_length = len(user_data)
            if user_data_length > 10:
                #get player's (last - 10) record
                user_data_len10 = user_data_length - 10
                actual=user_data[user_data_len10]
                first_date="".join(actual[1].split('-'))    #date and time of last - 10 record
                last_date="".join(user_data[user_data_length-1][1].split('-'))  #current date/time
                seconds_range=int(last_date)-int(first_date)  #how many seconds between player's commands
                if seconds_range < 30:  #player made more then 10 commands in range of 30 seconds. It is too quick, spam!
                    sql = """SELECT * FROM black_list
                            WHERE user = '"""+user+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()

                    row = []
                    for row in cur:
                        pass
                    if user not in row:   #user does not exist in 'black_list' table yet
                        sql = """INSERT INTO black_list
                            (user,date_time,count)
                            VALUES
                            (
                            '"""+user+"',strftime('%Y-%m-%d-%H-%M'),"+str(1)+"""
                            )                   
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:   #in row : exists in 'black_table'
                        count_ignore = row[3]
                        count_ignore = count_ignore + 1
                        sql = """UPDATE black_list
                                SET count = """+str(count_ignore)+", "+"""date_time = strftime('%Y-%m-%d-%H-%M')
                                WHERE user = '"""+user+"'"+""" 
                        """
                        cur.execute(sql)
                        conn.commit()
                    sql = """SELECT * FROM black_list
                        WHERE user = '"""+user+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()

                    row = []
                    for row in cur:
                        pass
                    if user in row:
                        ignore_count = row[3]
                        ignore_minutes = str(ignore_count)+'0'
                        check_ignore = '1'  #lock, start ignore        
                        self.send_reply( (user+", your actions are counted as spam, I'll ignore you for "+str(ignore_minutes)+" minutes"), user, channel )
                        return
### END OF SPAM FILTER
############    COMMADS:
            ### check if user is registered for privileged commands
            sql = """SELECT * FROM register
                    WHERE user = '"""+user+"'"+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            if user in row:     #user exists in 'register' table
                owner = row[3]
                authenticated = row[4]
                if (authenticated == 1):    #he is also authenticated           
                    ### All admin only commands go in here.
                    self.evalAdminCommand(command[0].lower(), user, channel, str(owner), str(authenticated))
                    
            cur.close()
                    
            ### All public commands go here
            self.evalCommand(command[0].lower(), user, channel)
#####
class BotCrashed(Exception): # Raised if the bot has crashed.
    pass

def main():
    # Here begins the main programs flow:
    connect_class = IRC_Server(config.server, config.port, config.bot_nick, config.channels.split(','))
    run_connect_class = multiprocessing.Process(None,connect_class.connect,name="IRC Server" )
    run_connect_class.start()
    ### run notification process
    if ( config.notifications == True ):
        print("Run 'notifications' process...")
        run_notify = multiprocessing.Process(None,notify.start(connect_class))
        run_notify.start()
    try:
        while(connect_class.should_reconnect):
            time.sleep(5)
        run_connect_class.join()
    except KeyboardInterrupt: # Ctrl + C pressed
        pass # We're ignoring that Exception, so the user does not see that this Exception was raised.
    if run_connect_class.is_alive:
        run_connect_class.terminate()
        run_connect_class.join() # Wait for terminate
    if run_connect_class.exitcode == 0 or run_connect_class.exitcode < 0:
        print("Bot exited.")
    else:
        raise BotCrashed("The bot has crashed")
