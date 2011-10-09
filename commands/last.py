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
Last Command Module: seen, activity, message, game
"""

import config
import sqlite3
import re
import time
import datetime
import config

def last(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) >= 3 ):
        if ( command[1].lower() == 'seen' ):
            seen(self, user, channel, command[2])
        elif ( command[1].lower() == 'activity' ):
            activity(self, user, channel, command[2:])
        

def seen_time( last_time, current ):
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

def seen(self, user, channel, request_user):
    
    """
    Shows when user was last seen on the channel
    """
    if ( "'" in request_user ):
        self.send_message_to_channel( ("Error! No such user in my database"), channel)
        return
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if re.search("^#", channel):
        user_nicks = self.parse_names(self.get_names(channel))
        if request_user in user_nicks:  #reciever is on the channel right now
            self.send_message_to_channel( ("User is online!"), channel)
            cur.close()
            return
        else:
            sql = """SELECT * FROM users
                    WHERE user = '"""+request_user+"'"+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            if request_user not in row:   #user not found
                self.send_message_to_channel( ("Error! No such user in my database"), channel)
            else:
                last_time = row[2]
                state = row[3]
                if state == True:
                    self.send_message_to_channel( ("User is somewhere online on IRC Network!"), channel)
                    cur.close()
                    return
                if ( last_time == None or last_time == '' ):
                    self.send_message_to_channel( ("Sorry, I don't have any record of when user left"), channel)
                else:
                    current = time.strftime('%Y-%m-%d-%H-%M-%S')
                    seen_result = seen_time( last_time, current )
                    if ( seen_result == '' ):
                        result = ' just now'
                    else:
                        result = seen_result + ' ago'
                    self.send_message_to_channel( (request_user + " was last seen" + result), channel)
    else:
        self.send_message_to_channel( ("You can use `]last seen` only on a channel"), user)
    cur.close()

def activity(self, user, channel, command_request):
    
    """
    Shows last user's activity (joins, quits, etc)
    """
    
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if re.search("^#", channel):
        usage = "Usage: " + config.command_prefix + "last activity [-c<amount of records>] username"
        if ( len(command_request) == 1 ):
            username = command_request[0]
            amount_records = '10'
        elif ( len(command_request) == 2 ):
            username = command_request[1]
            if ( command_request[0].startswith('-') ):
                amount_records = command_request[0][1:]
            else:
                self.send_reply( (usage), user, channel )
                cur.close()
                return
        else:
            self.send_reply( (usage), user, channel )
            cur.close()
            return
        if ( "'" in username ):
            self.send_notice("User is not found", user)
            cur.close()
            return
        sql = """SELECT act,date_time FROM activity
                WHERE user = '""" + username + """'
                LIMIT """ + amount_records + """
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):
            self.send_notice("No records of user's activity", user)
            cur.close()
            return
        else:
            for i in range(len(records)):
                if ( records[i][0] == 'join' ):
                    event = "Join"
                elif ( records[i][0] == 'part' ):
                    event = "Part"
                elif ( records[i][0] == 'quit' ):
                    event = "Quit"
                elif ( records[i][0] == 'nick' ):
                    event = "Change nick"
                last_time = records[i][1]
                current = time.strftime('%Y-%m-%d-%H-%M-%S')
                seen_result = seen_time( last_time, current )
                print(seen_result)
    else:
        self.send_message_to_channel( ("You can use `" + config.command_prefix + "last activity` only on a channel"), user)
    cur.close()
