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

def start(self, user, channel):
    string_command = (self.command)
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
            cur.close()
            return False
        else:   #no need to ignore, ignore_minutes < difference
            check_ignore = '0'
    if check_ignore == '0':
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
                    cur.close()
                    return False
    cur.close()
    return True
