#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This code was written for Python 3.1.1

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

import db_process
import notify
import commands
import admin_commands

# root admin
root_admin = "ihptru"
root_admin_password = "password" #only for the successful first run, dont forget to remove it later

###
if not os.path.exists('db/openra.sqlite'):
    db_process.start(root_admin, root_admin_password)
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

        str_buff = ( "JOIN %s \r\n" ) % (self.irc_channel)
        self.irc_sock.send (str_buff.encode())
        print ("Joining channel " + str(self.irc_channel) )
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
            if len(hours) == 1:
                real_hours = '0'+hours
            else:
                real_hours = hours
            if len(minutes) == 1:
                real_minutes = '0'+minutes
            else:
                real_minutes = minutes
            ### for logs end
            if str(recv).find ( "PING" ) != -1:
                self.irc_sock.send ( "PONG ".encode() + recv.split() [ 1 ] + "\r\n".encode() )             
             
            #recover all nicks on channel
            #if str(recv).find ( "353 orabot =" ) != -1:
            #    print (str(recv))
            #    user_nicks = str(recv).split(':')[2].rstrip()
            #    user_nicks = user_nicks.replace('+','').replace('@','')
            #    user_nicks = user_nicks.split(' ')
            #    self.nicks = user_nicks
            if str(recv).find ( "PRIVMSG" ) != -1:
                print(str(recv))
                irc_user_nick = str(recv).split ( '!' ) [ 0 ] . split ( ":")[1]
                irc_user_host = str(recv).split ( '@' ) [ 1 ] . split ( ' ' ) [ 0 ]
                irc_user_message = self.data_to_message(str(recv))
                # if PRIVMSG is still in string - message from person with ipv6
                suit = re.compile('PRIVMSG')
                if suit.search(irc_user_message):
                    irc_user_message = str(recv).split ( 'PRIVMSG' ) [ 1 ] . split ( ' :') [ 1: ]
                    irc_user_message = " ".join(irc_user_message)
                    irc_user_message = irc_user_message[:-5]
                ###logs
                chan = str(recv).split ( 'PRIVMSG' ) [ 1 ] . lstrip() . split(' :')[0]  #channel ex: #openra
                if self.irc_channel == '#openra' or self.irc_channel == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+irc_user_nick+': '+str(irc_user_message)+'\n'
                    if self.irc_channel == '#openra':
                        chan_d = 'openra'
                    elif self.irc_channel == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
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
                if ( str(irc_user_message[0]) == "]" ):
                    self.command = str(irc_user_message[1:])
                    # (str(recv)).split()[2] ) is simply the channel the command was heard on.
                    self.process_command(irc_user_nick, ( (str(recv)).split()[2] ))
### when message cotains link, show title
                if re.search('.*http.*://.*', str(irc_user_message)):
                    link = str(irc_user_message).split('://')[1].split()[0]
                    pre = str(irc_user_message).split('http')[1].split('//')[0]
                    link = 'http'+pre+'//'+link
                    if re.search('http.*youtube.com/watch.*', link):
                        if re.search("^#", chan):
                            link = link.split('&')[0]
                            try:
                                site = urllib.request.urlopen(link)
                                site = site.read()
                                site = site.decode('utf-8')
                                title = site.split('<title>')[1].split('</title>')[0].split('&#x202c;')[0].split('&#x202a;')[1].replace('&amp;','&').replace('&#39;', '\'').rstrip().lstrip()
                                if ( title != 'YouTube - Broadcast Yourself.' ):    #video exists
                                    self.send_message_to_channel( ("Youtube: "+title), chan )
                            except:
                                pass
                    else:
                        if re.search("^#", chan):
                            try:
                                site = urllib.request.urlopen(link)
                                site = site.read()
                                site = site.decode('utf-8')
                                title = site.split('<title>')[1].split('</title>')[0].rstrip().lstrip()
                                self.send_message_to_channel( ("Title: "+title), chan )
                            except:
                                pass
                        
###
            if str(recv).find ( "JOIN" ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                print (str(recv))
                irc_join_nick = str(recv).split( '!' ) [ 0 ].split( ':' ) [ 1 ]
                irc_join_host = str(recv).split( '!' ) [ 1 ].split( ' ' ) [ 0 ]
                #chan = str(recv).split( "JOIN" ) [ 1 ].lstrip().split( ":" )[1].rstrip()     #channle ex: #openra
                #chan = str(recv).split()[2].replace(':','').rstrip()
                sql = """SELECT * FROM users
                        WHERE user = '"""+irc_join_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if irc_join_nick not in row:     #user NOT found, add him (if user is not in db, he could not have ]later message)
                    #get last uid
                    sql = """SELECT * FROM users
                            ORDER BY uid DESC LIMIT 1
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    uid_users = row[0]
                    uid_users = uid_users + 1   # uid + 1
                    sql = """INSERT INTO users
                            (uid,user)
                            VALUES
                            (
                            """+str(uid_users)+",'"+str(irc_join_nick)+"'"+"""
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                else:   #he can have ]later messages
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
                            self.send_message_to_channel( (offline_message.replace("~qq~","'")), irc_join_nick )
                        time.sleep(0.1)
                        sql = """DELETE FROM later
                                WHERE reciever = '"""+irc_join_nick+"'"+"""
                        
                        """
                        
                        cur.execute(sql)
                        conn.commit()
                    sql = """UPDATE users
                            SET date = ''
                            WHERE user = '"""+irc_join_nick+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()
                    cur.close()
                ###logs
                if self.irc_channel == '#openra' or self.irc_channel == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+'* '+irc_join_nick+' ('+irc_join_host+') has joined '+self.irc_channel+'\n'
                    if self.irc_channel == '#openra':
                        chan_d = 'openra'
                    elif self.irc_channel == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                ###
            if str(recv).find ( "QUIT" ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                print (str(recv))
                irc_quit_nick = str(recv).split( "!" )[ 0 ].split( ":" ) [ 1 ]
                irc_quit_message = str(recv).split('QUIT :')[1].rstrip()
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
                        SET date = strftime('%Y-%m-%d-%H-%M-%S')
                        WHERE user = '"""+str(irc_quit_nick)+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                cur.close()
                ### for ]pick
                modes = ['1v1','2v2','3v3','4v4']
                diff_mode = ''
                for diff_mode in modes:
                    sql = """DELETE FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+irc_quit_nick+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                ##logs
                if self.irc_channel == '#openra' or self.irc_channel == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+'* '+irc_quit_nick+' has quit ('+irc_quit_message.rstrip()+')\n'
                    if self.irc_channel == '#openra':
                        chan_d = 'openra'
                    elif self.irc_channel == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
            if str(recv).find ( "PART" ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                print (str(recv))
                irc_part_nick = str(recv).split( "!" )[ 0 ].split( ":" ) [ 1 ]
                #chan = str(recv).split()[2].replace(':','')
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
                        SET date = strftime('%Y-%m-%d-%H-%M-%S')
                        WHERE user = '"""+str(irc_part_nick)+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                cur.close()
                ### for ]pick
                modes = ['1v1','2v2','3v3','4v4']
                diff_mode = ''
                for diff_mode in modes:
                    sql = """DELETE FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+irc_part_nick+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                ###logs
                if self.irc_channel == '#openra' or self.irc_channel == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+'* '+irc_part_nick+' has left '+self.irc_channel+'\n'
                    if self.irc_channel == '#openra':
                        chan_d = 'openra'
                    elif self.irc_channel == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                ###

        if self.should_reconnect:
            self.connect()

    def data_to_message(self,data):
        data = data[data.find(':')+1:len(data)]
        data = data[data.find(':')+1:len(data)]
        data = str(data[0:len(data)-5])
        return data

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
        if len(hours) == 1:
            real_hours = '0'+hours
        else:
            real_hours = hours
        if len(minutes) == 1:
            real_minutes = '0'+minutes
        else:
            real_minutes = minutes
        if channel == '#openra' or channel == '#openra-dev':
            row = '['+real_hours+':'+real_minutes+'] '+self.irc_nick+': '+str(data)+'\n'
            if channel == '#openra':
                chan_d = 'openra'
            elif channel == '#openra-dev':
                chan_d = 'openra-dev'
            else:
                chan_d = 'trash'
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
            # This needs to modify the list of active channels

    # This function takes a channel, which must start with a #.
    def quit_channel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "PART %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())
            # This needs to modify the list of active channels
    
    def evalAdminCommand(self, commandname, user, channel, owner, authenticated):
        if hasattr(admin_commands, commandname): #Command exists
            imp.reload(admin_commands)
            command_function=getattr(admin_commands, commandname)
            command_function(self, user, channel, owner, authenticated)
            
    def evalCommand(self, commandname, user, channel):
        if hasattr(commands, commandname): #Command exists
            imp.reload(commands)
            command_function=getattr(commands, commandname)
            command_function(self, user, channel)
            
    def process_command(self, user, channel):
        # This line makes sure an actual command was sent, not a plain "!"
        if ( len(self.command.split()) == 0):
            error = "Usage: ]command [arguments]"
            if re.search("^#", channel):
                self.send_message_to_channel( (error), channel)
            else:
                self.send_message_to_channel( (error), user)
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
            #get last uid_commands
            sql = """SELECT * FROM commands
                    ORDER BY uid DESC LIMIT 1
            """
            cur.execute(sql)
            conn.commit()
            
            for row in cur:
                pass
            uid_commands=row[0]
            
            uid_commands = uid_commands + 1
            #clear 'commands' table after each 1 000 000 record
            if uid_commands >= 1000:
                uid_commands = 1
                sql = """DELETE FROM commands WHERE uid > 1"""
                cur.execute(sql)
                conn.commit()
    
            #write each command into 'commands' table 
            sql = """INSERT INTO commands
                    (uid,user,command,date_time)
                    VALUES
                    (
                    """+str(uid_commands)+",'"+str(user)+"','"+string_command.replace("'","~qq~")+"',"+"strftime('%Y-%m-%d-%H-%M-%S')"+""" 
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
                        #get last uid_black_list

                        sql = """SELECT * FROM black_list
                                ORDER BY uid DESC LIMIT 1
                        """
                        cur.execute(sql)
                        conn.commit()
       
                        for row in cur:
                            pass
                        uid_black_list=row[0]
                        uid_black_list = uid_black_list + 1
                        
                        sql = """INSERT INTO black_list
                            (uid,user,date_time,count)
                            VALUES
                            (
                            """+str(uid_black_list)+",'"+user+"',strftime('%Y-%m-%d-%H-%M'),"+str(1)+"""
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
                        if re.search("^#", channel):
                            self.send_message_to_channel( (user+", your actions are counted as spam, I will ignore you for "+str(ignore_minutes)+" minutes"), channel )
                        else:
                            self.send_message_to_channel( (user+", your actions are counted as spam, I will ignore you for "+str(ignore_minutes)+" minutes"), user )
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
    test2 = IRC_Server("irc.freenode.net", 6667, "orabot", "#openra")
    test = IRC_Server("irc.freenode.net", 6667, "orabot", "#openra")
    run_test = multiprocessing.Process(None,test.connect,name="IRC Server" )
    run_test.start()
    ### run notification process
    run_notify = multiprocessing.Process(None,notify.start(test))
    run_notify.start()
    
    try:
        while(test.should_reconnect):
            time.sleep(5)
        run_test.join()
    except KeyboardInterrupt: # Ctrl + C pressed
        pass # We're ignoring that Exception, so the user does not see that this Exception was raised.
    if run_test.is_alive:
        run_test.terminate()
        run_test.join() # Wait for terminate
    if run_test.exitcode == 0 or run_test.exitcode < 0:
        print("Bot exited.")
    else:
        raise BotCrashed("The bot has crashed")
