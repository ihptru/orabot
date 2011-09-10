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

import config
import sqlite3
import re
import time
import datetime

def seen( last_time, current ):
    last_time = time.mktime(time.strptime( last_time, '%Y-%m-%d-%H-%M-%S'))
    current = time.mktime(time.strptime( current, '%Y-%m-%d-%H-%M-%S'))
    difference = current - last_time
    result = str(datetime.timedelta(seconds = difference))
    result = result.split(', ')
    if ( len(result) == 1 ):
        days = ''
        timest = result[0]
    else:
        days = ' ' + result[0]
        timest = result[1]
    timest = timest.split(':')
    result_string = days
    for i in range(len(timest)-1):
        if int(timest[i]) != 0:
            if ( ( timest[i][-1] == '1' ) and ( timest[i][-2:] != '11' ) ):
                end = ''
            else:
                end = 's'
            if i == 0:
                st = 'hour'
            elif i == 1:
                st = 'minute'
            st = st + end
            result_string = result_string + ' ' + str(int(timest[i])) + ' ' + st
    return result_string

def last(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        if re.search("^#", channel):
            #send NAMES channel to server
            str_buff = ( "NAMES %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())
            #recover all nicks on channel
            recv = self.irc_sock.recv( 4096 )
            recv=self.decode_stream(recv)
            if str(recv).find ( " 353 "+config.bot_nick ) != -1:
                user_nicks = str(recv).split(':')[2].rstrip()
                user_nicks = user_nicks.replace('+','').replace('@','')
                user_nicks = user_nicks.split(' ')
            
            if command[1] in user_nicks:  #reciever is on the channel right now
                self.send_message_to_channel( ("User is online!"), channel)
                cur.close()
                return
            else:
                sql = """SELECT * FROM users
                        WHERE user = '"""+command[1]+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if command[1] not in row:   #user not found
                    self.send_message_to_channel( ("Error! No such user in my database"), channel)
                else:
                    last_time = row[2]
                    state = row[3]
                    if state == True:
                        self.send_message_to_channel( ("User is somewhere online on IRC Network!"), channel)
                        return
                    if ( last_time == None or last_time == '' ):
                        self.send_message_to_channel( ("Sorry, I don't have any record of when user left"), channel)
                    else:
                        current = time.strftime('%Y-%m-%d-%H-%M-%S')
                        seen_result = seen( last_time, current )
                        if ( seen_result == '' ):
                            result = ' just now'
                        else:
                            result = seen_result + ' ago'
                        self.send_message_to_channel( (command[1]+" was last seen"+result), channel)
        else:
            self.send_message_to_channel( ("You can use ]last only on a channel"), user)
    elif ( len(command) == 1 ):
        self.send_reply( ("Usage: ]last nick"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()
