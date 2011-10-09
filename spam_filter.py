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

import sqlite3
from datetime import date
import time
import datetime

def start(self, user, channel):
    string_command = (self.command)
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    sql = """SELECT date_time,count FROM black_list
        WHERE user = '"""+user+"'"+"""
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    if ( len(records) != 0 ):
        ignore_minutes = str(records[0][1]) + '0'
        ignore_seconds = int(ignore_minutes) * 60
        ignore_date = time.mktime(time.strptime( records[0][0], '%Y-%m-%d-%H-%M-%S'))  #in seconds
        current = time.strftime('%Y-%m-%d-%H-%M-%S')
        current_date = time.mktime(time.strptime( current, '%Y-%m-%d-%H-%M-%S'))    #in seconds
        difference = current_date - ignore_date  #how many seconds after last ignore
        if ( difference < ignore_seconds ):
            cur.close()
            # Ignore
            return False
    sql = """SELECT uid FROM commands
            ORDER BY uid LIMIT 1010
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    #clear 'commands' table after each 1 000 record
    if ( len(records) >= 1000 ):
        sql = """DELETE FROM commands WHERE uid > 30"""
        cur.execute(sql)
        conn.commit()

    #write each command into 'commands' table
    sql = """INSERT INTO commands
            (user,command,date_time)
            VALUES
            (
            '"""+user+"','"+string_command.replace("'","''")+"',"+"strftime('%Y-%m-%d-%H-%M-%S')"+""" 
            )
    """
    cur.execute(sql)
    conn.commit()

    #extract last 30 records
    sql = """SELECT * FROM commands
        ORDER BY uid DESC LIMIT 30
    """
    cur.execute(sql)

    var = []
    for row in cur:
        var.append(row)
    var.reverse()
    actual = []
    user_data = []
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
        actual = user_data[user_data_len10]
        first_date = actual[1]    #date and time of last - 10 record
        first_date = time.mktime(time.strptime( first_date, '%Y-%m-%d-%H-%M-%S'))
        last_date = user_data[user_data_length-1][1]  #current date/time (of last command by that user)
        last_date = time.mktime(time.strptime( last_date, '%Y-%m-%d-%H-%M-%S'))
        seconds_range = last_date - first_date  #how many seconds between player's commands
        if seconds_range < 60:  #more than 10 commands per minute. It is too quick, spam!
            sql = """SELECT user FROM black_list
                    WHERE user = '"""+user+"'"+"""
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()

            if ( len(records) == 0 ):   #user does not exist in 'black_list' table yet
                sql = """INSERT INTO black_list
                    (user,date_time,count)
                    VALUES
                    (
                    '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),"+str(6)+"""
                    )                   
                """
                cur.execute(sql)
                conn.commit()
            else:   #in row : exists in 'black_table'
                count_ignore = row[3]
                count_ignore = count_ignore + 6
                sql = """UPDATE black_list
                        SET count = """+str(count_ignore)+", "+"""date_time = strftime('%Y-%m-%d-%H-%M-%S')
                        WHERE user = '"""+user+"'"+""" 
                """
                cur.execute(sql)
                conn.commit()
            sql = """SELECT count FROM black_list
                WHERE user = '"""+user+"'"+"""
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( len(records) != 0 ):
                ignore_count = records[0][0]
                ignore_minutes = str(ignore_count) + '0'
                self.send_reply( (user+", your actions are counted as spam, I'll ignore you for "+str(ignore_minutes)+" minutes"), user, channel )
                cur.close()
                return False
    cur.close()
    return True
