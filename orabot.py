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

import socket
import multiprocessing
import time
import os
import re
import sqlite3
import urllib.request
import imp
import html.parser
import json

import db_initialization
import config
import handle_commands
# IRC events in 'irc/' directory
from irc import *
# load all tools
from tools import *

# Defining a class to run the server. One per connection
class IRC_Server:

    def __init__(self, host, port, nick, channels,
                    nickserv, nickserv_password,
                    command_prefix, command_timeout,
                    write_logs, log_channels,
                    tools_support, log_dir,
                    do_not_support_commands):
        self.irc_host = host
        self.irc_port = port
        self.irc_nick = nick
        self.channels = channels
        self.nickserv = nickserv
        self.nickserv_password = nickserv_password
        self.command_prefix = command_prefix
        self.command_timeout = command_timeout
        self.write_logs = write_logs
        self.log_channels = log_channels
        self.tools_support = tools_support
        self.log_dir = log_dir
        self.do_not_support_commands = do_not_support_commands

        self.irc_sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.is_connected = False
        self.listen_return = ''
        self.connect_return = ''
        self.command = ""
        self.start_time = time.mktime(time.strptime( time.strftime('%Y-%m-%d-%H-%M-%S'), '%Y-%m-%d-%H-%M-%S'))
        self.last_lines = []    # keep in memory last 20 messages (including username and his message)
        self.close_threads = [0]

    def __del__(self):
        self.irc_sock.close()

    def ircbot(self):
        # Create database at first run
        if not os.path.exists('db/'+self.irc_host+'.sqlite'):
            db_initialization.start(self)
        try:
            while True:
                conn, cur = self.db_data()
                sql = """UPDATE users
                        SET state = 0;
                        DELETE FROM user_channel;
                """
                cur.executescript(sql)
                conn.commit()
                cur.close()
                if self.tools_support:
                    fns = [openra_topic.start, openra_bugs.start]
                    procs = [multiprocessing.Process(target=f, args=(self,)) for f in fns]
                    print(("*** [%s] Tools are supported") % (self.irc_host))
                    self.tools('start', procs)

                if self.connect():
                    if ( self.connect_return == 'Excess Flood' ):
                        if self.tools_support:
                            self.tools('terminate', procs)
                            print("*** [%s] Terminated child processes" % self.irc_host)
                        print("*** [%s] Restarting the bot" % self.irc_host)
                        time.sleep(5)
                        self.irc_sock.close()
                        continue
                    elif ( self.connect_return == 'Manual Quit' ):
                        if self.tools_support:
                            self.tools('terminate', procs)
                            print("*** [%s] Terminated child processes" % self.irc_host)
                        print("*** [%s] Exit" % self.irc_host)
                        break
                self.close_threads = [1]
        except KeyboardInterrupt:
            self.close_threads = [1]
            raise KeyboardInterrupt

    def tools(self, action, procs):
        if ( action == 'start' ):
            for p in procs:
                p.start()
        elif ( action == 'terminate' ):
            for p in procs:
                p.terminate()

    # This is the bit that controls connection to a server & channel.
    def connect(self):
        try:
            self.irc_sock.connect ((self.irc_host, self.irc_port))
        except:
            print ("*** [%s] Error: Could not connect to IRC server on (%s) port!" % (self.irc_host, self.irc_port))
            exit(1) # We should make it recconect if it gets an error here
        print ("*** [%s] Connected to IRC server on (%s) port" % (self.irc_host, self.irc_port))

        def bot_connect(self):
            str_buff = ("NICK %s \r\n") % (self.irc_nick)
            self.irc_sock.send (str_buff.encode())
            print (("*** [%s] Setting bot nick to " + str(self.irc_nick)) % (self.irc_host))

            str_buff = ("USER %s 8 * :X\r\n") % (self.irc_nick)
            self.irc_sock.send (str_buff.encode())

            for channel in self.channels:
                str_buff = ( "JOIN %s \r\n" ) % (channel)
                self.irc_sock.send (str_buff.encode())
                print (("*** [%s] Joining channel " + channel) % (self.irc_host))
        bot_connect(self)
        
        if self.nickserv == True:
            print (("*** [%s] Sending request to identify with NickServ...") % (self.irc_host))
            data = "identify "+self.nickserv_password
            self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % ('NickServ', data)).encode() )

        self.is_connected = True
        while True:
            if self.listen():
                if ( self.listen_return == 'Nick in Use' ):
                    self.irc_nick = self.irc_nick + "_"
                    bot_connect(self)
                    continue
                elif ( self.listen_return == 'Manual Quit' ):
                    self.is_connected = False
                    self.connect_return = 'Manual Quit'
                    return True
                elif ( self.listen_return == 'Excess Flood' ):
                    self.connect_return = 'Excess Flood'
                    return True

    def listen(self):
        while self.is_connected:
            recv = self.irc_sock.recv( 4096 )
            recv = self.decode_stream( recv )

            data = self.handle_recv( recv )
            for recv in data:
                try:
                    framed_recv = recv.split()
                    if len(framed_recv) < 2:
                        continue
                except:
                    continue
                if framed_recv[0] == "PING":
                    self.irc_sock.send ( ("PONG " + framed_recv[1] + "\r\n").encode() )

                elif framed_recv[1] == "PRIVMSG":
                    user_nick = recv.split ( '!' ) [ 0 ] . split ( ":")[1]
                    user_message = self.data_to_message(recv)
                    channel = (recv).split()[2]
                    if (len(self.last_lines) >= 20):
                        for i in range(3):
                            self.last_lines.pop(0)
                    self.last_lines.append((user_nick.lower(), user_message))
                    imp.reload(privmsg_e)
                    multiprocessing.Process(target=privmsg_e.parse_event,
                                            args=(self,user_nick,user_message,channel,)).start()

                elif framed_recv[1] == "JOIN":
                    imp.reload(join_e)
                    join_e.parse_event(self, recv)

                elif framed_recv[1] == "QUIT":
                    nick = recv.split('!')[0][1:]
                    message = " ".join(framed_recv[2:])[1:]
                    if ( nick == self.irc_nick ):
                        print("*** [%s] Disconnected" % self.irc_host)
                        if ( message == 'Excess Flood' ):
                            self.listen_return = 'Excess Flood'
                            return True
                        else:
                            self.listen_return = 'Manual Quit'
                            return True
                    imp.reload(quit_e)
                    quit_e.parse_event(self, recv)

                elif framed_recv[1] == "PART":
                    imp.reload(part_e)
                    part_e.parse_event(self, recv)

                elif framed_recv[1] == "NICK":
                    imp.reload(nick_e)
                    nick_e.parse_event(self, recv)

                elif framed_recv[1] == "NOTICE" and framed_recv[2].startswith("#"):
                    imp.reload(channel_notice_e)
                    channel_notice_e.parse_event(self, recv)

                elif framed_recv[1] == "TOPIC":
                    imp.reload(topic_e)
                    topic_e.parse_event(self, recv)

                elif framed_recv[1] == "KICK":
                    if framed_recv[3] == self.irc_nick:
                        print(("*** [%s] %s kicked me from %s!!!") %
                                    (self.irc_host, framed_recv[0].split(':')[1].split('!')[0], framed_recv[2]))
                    imp.reload(kick_e)
                    kick_e.parse_event(self, recv)

                elif framed_recv[1] == "MODE":
                    if ( framed_recv[0] != ":" + self.irc_nick ):
                        if framed_recv[3] in ['+v','-v','+o','-o','+h','-h']:
                            imp.reload(mode_e)
                            mode_e.parse_event(self, recv)

                elif framed_recv[1] == "353" and framed_recv[2] == self.irc_nick:   # NAMES request by bot
                    imp.reload(names_e)
                    names_e.parse_event(self, recv)

                elif framed_recv[1] == "NOTICE" and framed_recv[2] == self.irc_nick and framed_recv[6] == "identified":
                    print(("*** [%s] NickServ Identification Succeeded\t\tOK") % (self.irc_host))

                elif framed_recv[1] == "433" and framed_recv[3] == self.irc_nick:
                    print(("*** [%s] Nick is already in use!") % (self.irc_host))
                    self.listen_return = 'Nick in Use'
                    return True
                
                elif framed_recv[1] == "471":
                    channel = recv.split()[3]
                    print (("*** [%s] %s is full!") % (self.irc_host, channel))

                elif framed_recv[1] == "473":
                    channel = recv.split()[3]
                    print (("*** [%s] %s is invite only!") % (self.irc_host, channel))

                elif framed_recv[1] == "474":
                    channel = recv.split()[3]
                    print (("*** [%s] Bot is banned from %s!") % (self.irc_host, channel))

                elif framed_recv[1] == "475":
                    channel = recv.split()[3]
                    print (("*** [%s] Key is required for %s !") % (self.irc_host, channel))

                elif framed_recv[1] == "401" and framed_recv[2] == self.irc_nick: # no such nick/channel
                    imp.reload(e_401)
                    e_401.parse_event(self, recv)

                elif framed_recv[0] == "ERROR" and framed_recv[1] == ":Closing":
                    print (("*** [%s] Connection aborted!") % (self.irc_host))
                    exit(1)

    def data_to_message(self, data):
        data = data[data.find(" :")+2:]
        return data

    #handle as single line request as multiple ( split recv into pieces before processing it )
    def handle_recv(self, recv):
        regex = re.compile('(.*?)\r\n')
        recv = regex.findall(recv)
        return recv

    def decode_stream(self, stream):
        try:
            return stream.decode("utf-8")
        except:
            return stream.decode("CP1252")

    def send_reply(self, data, user, channel):
        target = channel if channel.startswith('#') else user
        self.send_message_to_channel(data, target)

    # This function sends a message to a channel or user
    def send_message_to_channel(self, data, channel):
        print ( ( "[%s %s] %s: %s") % (self.irc_host, channel, self.irc_nick, data) )
        self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % (channel, data[0:512])).encode() )
        self.logs(self.irc_nick, channel, 'privmsg', str(data), '')

    def send_notice(self, data, user):
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,data)
        self.irc_sock.send (str_buff.encode())
        print ( ( "*** [%s] NOTICE to %s: %s" ) % (self.irc_host, user, data) )

    def send_names(self, channel):
        str_buff = ( "NAMES %s \r\n" ) % (channel)
        self.irc_sock.send (str_buff.encode())

    def get_names(self, channel):
        conn, cur = self.db_data()
        sql = """SELECT user FROM user_channel
                WHERE channel = '"""+channel+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        cur.close()
        names = []
        for i in range(len(records)):
            names.append(records[i][0])
        return names

    def db_data(self):
        conn = sqlite3.connect('db/'+self.irc_host+'.sqlite')   # connect to database
        cur = conn.cursor()
        return (conn, cur)

    def join_channel(self, channel):
        if (channel[0] == "#"):
            str_buff = ( "JOIN %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())

    def quit_channel(self, channel):
        if (channel[0] == "#"):
            conn, cur = self.db_data()
            sql = """SELECT user FROM user_channel
                    WHERE channel = '"""+channel+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            name_this_channel = []  # users on specified channel
            for i in range(len(records)):
                name_this_channel.append(records[i][0])
            sql = """SELECT user FROM user_channel
                    WHERE channel <> '"""+channel+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            name_other_channels = []    # users on other channel
            if len(records) != 0:
                for i in range(len(records)):
                    name_other_channels.append(records[i][0])
            for n in name_this_channel:
                if ( n not in name_other_channels ):
                    sql = """UPDATE users
                            SET state = 0
                            WHERE user = '"""+n.lower()+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
            sql = """DELETE FROM user_channel
                    WHERE channel = '"""+channel+"""'
            """
            cur.execute(sql)
            conn.commit()
            cur.close()
            str_buff = ( "PART %s \r\n" ) % (channel)
            self.irc_sock.send ( str_buff.encode() )

    def topic(self, channel, topic):
        str_buff = ("TOPIC %s :%s\r\n") % (channel, topic)
        self.irc_sock.send ( str_buff.encode() )

        conn, cur = self.db_data()
        sql = """SELECT status FROM user_channel
                WHERE user = '"""+self.irc_nick.lower()+"""' AND channel = '"""+channel+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):   # bot must be on a channel to send warning message
            if ( records[0][0] == '' or records[0][0] == None ):    # bot is not Op/HalfOp/Voice
                self.send_message_to_channel( ("Tried to change the topic of channel but do not have rights"), channel)
        cur.close()

    def kick_user(self, user, channel, reason):
        str_buff = ( "KICK %s %s :%s\r\n" ) % (channel, user, reason)
        self.irc_sock.send ( str_buff.encode() )    # will work if bot has OP

    def logs(self, irc_user, channel, logs_of, some_data, some_more_data):
        if self.write_logs == True:
            chan_d = str(channel).replace('#','')
            t = time.localtime( time.time() )
            time_prefix = time.strftime( '%Y-%m-%dT%T', t )
            log_dir = self.log_dir
            if ( log_dir[-1] != '/' ):
                log_dir = log_dir + '/'
            filename = log_dir + self.irc_host + '/' + chan_d + time.strftime( '/%Y/%m/%d', t )
            if channel in self.log_channels.split():
                if ( logs_of == 'privmsg' ):
                    row = ' <'+irc_user+'> '+some_data+'\n'
                elif ( logs_of == 'action' ):
                    row = ' * '+irc_user+' '+some_data+'\n'
                elif ( logs_of == 'join' ):
                    row = ' *** '+irc_user+' <'+some_data+'> has joined '+channel+'\n'
                elif ( logs_of == 'quit' ):
                    row = ' *** '+irc_user+' <'+some_data+'> has quit IRC'+some_more_data+'\n'
                elif ( logs_of == 'part' ):
                    row = ' *** '+irc_user+' <'+some_data+'> has left '+channel+'\n'
                elif ( logs_of == 'nick' ):
                    row = ' *** '+irc_user+' is now known as '+some_data+'\n'
                elif ( logs_of == 'topic' ):
                    row = ' *** '+irc_user+' changes topic to "'+some_data+'"\n'
                elif ( logs_of == 'kick' ):
                    row = ' *** '+irc_user+' was kicked by '+some_data+' ('+some_more_data+')\n'
                elif ( logs_of == 'mode' ):
                    row = ' *** '+some_data+'\n'
                elif ( logs_of == 'channel_notice'):
                    row = ' *** NOTICE to '+channel+' from '+irc_user+': '+some_data+'\n'
                else:
                    return  # probably an error.
                dir = os.path.dirname(filename)
                try:
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(time_prefix + row)
                    file.close()
                except:
                    print(('*** [%s] Error! No write permissions to logs dir! (or ascii error)') (self.irc_nick))

    def parse_html(self, string):
        h = html.parser.HTMLParser()
        string = h.unescape(string)
        return string.strip()

    def data_from_url(self, url, bytes):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')] # fake our user-agent
        data = opener.open(url).read(bytes)
        try:
            encoding = str(data).lower().split('charset=')[1].split('"')[0]
            data = data.decode(encoding)
        except: # encoding was not found
            data = data.decode('utf-8')
        return data

    def title_from_url(self, url):
        data = self.data_from_url(url, 8192) # size should be enough
        rx_title = re.compile(r'<title>(.*?)</title>', re.IGNORECASE)
        titles = rx_title.findall(data.replace('\n',' '))
        if ( titles != [] ):
            title = self.parse_html(titles[0])
            return title
        else:
            raise Exception(("*** [%s] Exception: %s does not contain title") % (self.irc_host, url))

    def parse_link(self, channel, user, message):
        if re.search('.*http.*://.*', message):
            
            def check_localnetwork(self, url):
                if re.search('127.*', url):
                    return True
                if re.search('192.168.*', url):
                    return True
                if url == 'localhost':
                    return True
                if re.search('10\..*', url):
                    return True
                return False
            
            matches = re.findall(r"http.?://[^\s]*", message)
            mentioned = []
            for http_link in matches:
                if http_link in mentioned:
                    continue
                mentioned.append(http_link)
                link = http_link.split('://')[1]
                if check_localnetwork(self, link):
                    return
                pre = http_link.split('http')[1].split('//')[0]
                link = 'http'+pre+'//'+link
                if re.search("^#", channel):
                    youtube_match = re.findall('.*youtube.*v=(.+)', http_link)
                    if len(youtube_match) != 0:
                        v = youtube_match[0].split('&')[0]
                        link = 'http://www.youtube.com/watch?v='+v
                        try:
                            title = self.title_from_url(link).split('- YouTube')[0]
                            if ( title != 'YouTube - Broadcast Yourself.' ):    #video exists
                                self.send_message_to_channel( ("Youtube: " + title), channel )
                        except Exception as e:  # socket error or 404 error in title_from_url() or title not found
                            print(("*** [%s] %s") % (self.irc_host, e))
                    else:
                        try:
                            title = self.title_from_url(link)
                            self.send_message_to_channel( ("Title: " + title), channel )
                        except Exception as e:  # socket error or 404 error in title_from_url() or title not found
                            print(("*** [%s] %s") % (self.irc_host, e))

    def parse_bug_num(self, channel, message):
        matches = re.findall(r"\B"+"#([0-9]*)", message)
        mentioned = []
        if ( matches != [] ):
            if re.search("^#", channel):
                for bug_report in matches:
                    if ( bug_report == '' ):
                        return
                    if ( bug_report in mentioned):
                        continue
                    mentioned.append(bug_report)
                    url = 'https://api.github.com/repos/OpenRA/OpenRA/issues/'+bug_report   #api v3
                    try:
                        data = urllib.request.urlopen(url).read().decode()
                        y = json.loads(data)
                        type = "Issue"
                        if y['pull_request']['html_url'] != None:
                            type = "Pull request"
                        self.send_message_to_channel( ("%s #%s(%s) by %s: %s | http://bugs.open-ra.org/%s") %
                                (type, bug_report, y['state'], y['user']['login'], y['title'], bug_report), channel)
                    except Exception as e:
                        print(("*** [%s] %s") % (self.irc_host, e))

    def safe_eval(self, expr, symbols={}):
            return eval(expr, dict(__builtins__=None), symbols)

    # This function is for pickup matches code
    def players_for_mode(self, mode):
        return sum( map( int, mode.split('v') ) )

    # Special admin commands for Op/HalfOp/Voice
    def Admin(self, user, channel):
        if ( not channel.startswith('#') ):
            self.send_reply( ("Admin commands can be used only on a channel!"), user, channel )
            return False
        conn, cur = self.db_data()
        sql = """SELECT status FROM user_channel
                WHERE user = '"""+user.lower()+"""' AND channel = '"""+channel+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( records[0][0] == '' or records[0][0] == None ):
            self.send_reply( ("No rights!"), user, channel )
            return False
        return True

    def spam_filter(self, user, channel):
        if self.last_lines.count(self.last_lines[-1]) >= 10:
            reason = "stop spamming channel, please!"
            self.kick_user(user, channel, reason)

    def process_command(self, user, channel):
        command = (self.command).split()
        # The command isn't case sensitive
        if ( len(command) == 0):
            error = "Usage: "+self.command_prefix+"command [arguments]"
            self.send_reply( (error), user, channel )
            return
        if command[0].lower() in self.do_not_support_commands.split():
            return
        imp.reload(handle_commands)    # will re-import all existing commands in realtime
        handle_commands.evalCommand(self, command[0].lower(), user, channel)

def main():
    # Here begins the main programs flow:
    try:
        for irc_server in config.servers:
            server_data = eval('config.'+irc_server)
            ircserver = IRC_Server(server_data['host'],
                                    server_data['port'],
                                    server_data['bot_nick'],
                                    server_data['channels'].split(),
                                    server_data['nickserv'],
                                    server_data['nickserv_password'],
                                    server_data['command_prefix'],
                                    server_data['command_timeout'],
                                    server_data['write_logs'],
                                    server_data['log_channels'],
                                    server_data['tools_support'],
                                    server_data['log_dir'],
                                    server_data['do_not_support_commands'])
            ircserver_process = multiprocessing.Process(None, ircserver.ircbot, name="IRC Server")
            ircserver_process.start()
    except KeyboardInterrupt:
        exit(1)
