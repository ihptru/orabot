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
import time

def start(self, user, channel):
    string_command = (self.command)
    conn, cur = self.db_data()
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
            ORDER BY uid LIMIT 1001
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    #clear 'commands' table after each 1 000 record
    if ( len(records) >= 1000 ):
        sql = """DELETE FROM commands WHERE uid <= (SELECT max(uid)-30 FROM commands)"""
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
    sql = """SELECT user,date_time FROM commands
            ORDER BY uid DESC LIMIT 30
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    
    user_record = []
    records.reverse()
    for i in range(30):
        if ( user in records[i][0] ):
            user_record.append(records[i][0:])
    if ( len(user_record) > 10 ):
        first_date = user_record[-10:][0][1]    #date and time of last - 10 record
        first_date = time.mktime(time.strptime( first_date, '%Y-%m-%d-%H-%M-%S'))
        last_date = user_record[-1][1]  #current date/time (of last command by that user)
        last_date = time.mktime(time.strptime( last_date, '%Y-%m-%d-%H-%M-%S'))
        seconds_range = last_date - first_date  #how many seconds between player's commands
        if seconds_range < 60:  #more than 10 commands per minute. It is too quick, spam!
            sql = """SELECT user,count FROM black_list
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
                count_ignore = int(records[0][1])
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
                ignore_hours = str(int(int(ignore_minutes) / 60))
                if ( ignore_hours == '1' ):
                    hour = ' hour'
                else:
                    hour = ' hours'
                self.send_reply( (user+", your actions are counted as spam, I'll ignore you for " + ignore_hours + hour), user, channel )
                cur.close()
                return False
    cur.close()
    return True
