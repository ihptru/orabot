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

import time
import sqlite3
import urllib.request
import re
from datetime import date

def get_commits():
    url = 'https://github.com/chrisforbes/OpenRA/commits/master'
    titles = []
    try:
        stream = urllib.request.urlopen(url).read().decode('utf-8')
    except:
        return titles
    commits = stream.split('<p class="commit-title">')
    amount_commits = len(commits)
    for i in range(amount_commits):
        commit_title = commits[i].split('</a>')[0].split('">')[1].strip()
        titles.append(commit_title)
    return titles

def check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user):
    notify_message = "New game: "+name+" - mod: "+mod+version+" - Already "+players+" players in"
    if ( db_timeout.lower() == 'all' ):
        self.send_reply( (notify_message), db_user, db_user )
    elif ( db_timeout.lower() == 'till_quit' ):
        self.send_reply( (notify_message), db_user, db_user )
    else:
        date_of_adding = int(db_date.replace('-',''))
        ###
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
            hours = '0'+hours
        else:
            hours = hours
        if len(minutes) == 1:
            minutes = '0'+minutes
        else:
            minutes = minutes
        if len(seconds) == 1:
            seconds = '0'+seconds
        else:
            seconds = seconds
        localtime = year+month+day+hours+minutes+seconds
        localtime = int(localtime)
        difference = localtime - date_of_adding     #in result - must be less then timeout
        if ( db_timeout[-1] == 's' ):
            timeout = db_timeout[0:-1]
        elif ( db_timeout[-1] == 'm' ):
            timeout = int(db_timeout[0:-1]+'00')
        elif ( db_timeout[-1] == 'h' ):
            timeout = int(db_timeout[0:-1]+'0000')
        elif ( db_timeout[-1] == 'd' ):
            timeout = int(db_timeout[0:-1]+'000000')
        if ( difference < timeout ):
            self.send_reply( (notify_message), db_user, db_user )
        else:   # timeout is over
            sql = """DELETE from notify
                    WHERE user = '"""+db_user+"""'
            """
            cur.execute(sql)
            conn.commit()
        ###

def start(self):
    notify_ip_list = []
    notify_players_list = []
    bugreport_var = 0
    commit_var = 0
    
    def update_commits(titles):
        conn = sqlite3.connect('../db/openra.sqlite')
        cur = conn.cursor()
        sql = """DELETE FROM commits
        """
        cur.execute(sql)
        conn.commit()
        for i in range(len(titles)):
            sql = """INSERT INTO commits
                    (title)
                    VALUES
                    (
                    '"""+titles[i].replace("'","''")+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
        cur.close()
        print("Commits Table Updated...")

    titles = get_commits()
    if ( len(titles) == 0 ):
        print("### Something went wrong fetching commits info! ### Clearing commits table...")
        conn = sqlite3.connect('../db/openra.sqlite')
        cur = conn.cursor()
        sql = """DELETE FROM commits
        """
        cur.execute(sql)
        conn.commit()
        cur.close()
    else:
        update_commits(titles)

    while True:
        time.sleep(5)
        bugreport_var = bugreport_var + 1
        commit_var = commit_var + 1
        ### commits
        if ( commit_var == 50 ):
            commit_var = 0
            def commits(self):
                flood_protection = 0
                conn = sqlite3.connect('../db/openra.sqlite')
                cur = conn.cursor()
                sql = """SELECT title FROM commits
                """
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                titles = get_commits()
                if ( len(titles) == 0 ):
                    return
                if ( len(records) == 0 ):   #There was an error at notification's start (probably fetching error(caused by socket)), so `commits` table is clear
                    ### current fetch is full of commits, so we fill table; return; do not notify
                    for i in range(len(titles)):
                        sql = """INSERT INTO commits
                                (title)
                                VALUES
                                (
                                '"""+titles[i].replace("'","''")+"""'
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                    return
                commits_to_show = []
                existing_commits = []
                for i in range(len(records)):
                    existing_commits.append(records[i][0])
                for i in range(len(titles)):
                    if titles[i] not in existing_commits:
                        commits_to_show.append(titles[i])
                commits_to_show.reverse()
                for i in range(len(commits_to_show)):
                    flood_protection = flood_protection + 1
                    if flood_protection == 5:
                        time.sleep(5)
                        flood_protection = 0
                    self.send_message_to_channel( ("News from github: "+commits_to_show[i]), '##orabot-test-channel' )
                flood_protection = 0

            commits(self)
        ### bugreport part:
        if ( bugreport_var == 100 ):
            bugreport_var = 0
            def bugreport(self):
                url = 'http://bugs.open-ra.org/projects/openra/issues.atom'
                try:
                    stream = urllib.request.urlopen(url).read()
                except:
                    return
                bug_report_title = str(stream).split('<entry>')[1].split('<title>')[1].split('</title>')[0]
                bug_report_issue = str(stream).split('<entry>')[1].split('<link href="')[1].split('" rel=')[0].split('/')[-1]
                bug_report_url = 'http://bugs.open-ra.org/issues/'+bug_report_issue
                filename = 'bug_report.txt'
                line = []
                try:
                    file = open(filename, 'r')
                    line = file.readlines()
                    file.close()
                except:
                    pass
                if ( bug_report_title.split()[1]+'\n' not in line ):
                    filename = 'bug_report.txt'
                    file = open(filename, 'a')
                    file.write(bug_report_title.split()[1]+"\n")
                    file.close()
                    message = bug_report_title+" | "+bug_report_url
                    self.send_message_to_channel( (message), '#openra' )
            bugreport(self)
        ### new game notifications part
        ip_current_games = []
        players_current_games = []
        timeouts = ['s','m','h','d']
        flood_protection = 0
        url = 'http://master.open-ra.org/list.php'
        try:
            stream = urllib.request.urlopen(url).read()
        except:
            continue
        if ( stream != b'' ):
            split_games = str(stream).split('\\nGame')
            length_games = len(split_games)
            for i in range(int(length_games)):
                ip = split_games[i].split('\\n\\t')[3].split()[1].split(':')[0]
                
                ip_current_games.append(ip)
                
                state = split_games[i].split('\\n\\t')[4]
                players = split_games[i].split('\\n\\t')[5].split()[1]
                
                players_current_games.append(players)
                
                name = " ".join(split_games[i].split('\\n\\t')[2].split()[1:])
                mod = split_games[i].split('\\n\\t')[7].split()[1].split('@')[0]
                try:
                    version = " - version: " + split_games[i].split('\\n\\t')[7].split()[1].split('@')[1]
                except:
                    version = ''    #no version in output
                down = name.split('[down]')
                if ( ip in notify_ip_list ):
                    if ( state == 'State: 2' ):
                        #game in list but started, remove from `notify_ip_list`
                        ip_index = notify_ip_list.index(ip)
                        del notify_ip_list[ip_index]
                        del notify_players_list[ip_index]
                        ip_index = ip_current_games.index(ip)
                        del ip_current_games[ip_index]
                        del players_current_games[ip_index]
                    elif ( state == 'State: 1' ):   #needed to check if amount of player is increased to number, users are subscribed for
                        ip_index_previous = notify_ip_list.index(ip)
                        ip_index_current = ip_current_games.index(ip)
                        if ( len(down) == 1 ):  #game is not [down]
                            conn = sqlite3.connect('../db/openra.sqlite')
                            cur = conn.cursor()
                            sql = """SELECT user,date,mod,version,timeout,num_players FROM notify
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            data = []
                            for row in cur:
                                data.append(row)
                            if ( data != [] ):
                                length_data = len(data)
                                for i in range(int(length_data)):
                                    flood_protection = flood_protection + 1
                                    if flood_protection == 5:
                                        time.sleep(5)
                                        flood_protection = 0
                                    db_user = data[i][0]
                                    db_date = data[i][1]
                                    db_mod = data[i][2]
                                    db_version = data[i][3]
                                    db_timeout = data[i][4]
                                    db_num_players = data[i][5]
                                    if ( db_mod.lower() == mod or db_mod.lower() == 'all' ):
                                        if ( re.search(db_version, version) or db_version.lower() == 'all' ):
                                            try:
                                                db_num_players = int(db_num_players)
                                                if db_num_players > int(notify_players_list[ip_index_previous]) and db_num_players <= int(players_current_games[ip_index_current]):
                                                    check_num_players = True
                                                else:
                                                    check_num_players = False
                                            except:
                                                check_num_players = False
                                            if ( check_num_players == True ):
                                                check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user)
                                flood_protection = 0
                else:   #ip is not in a list
                    if ( state == 'State: 1' ):
                        notify_ip_list.append(ip)
                        notify_players_list.append(players)
                        if ( len(down) == 1 ):  #game is not [down]
                            conn = sqlite3.connect('../db/openra.sqlite')
                            cur = conn.cursor()
                            sql = """SELECT user,date,mod,version,timeout,num_players FROM notify
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            data = []
                            for row in cur:
                                data.append(row)
                            if ( data != [] ):
                                length_data = len(data)
                                for i in range(int(length_data)):
                                    flood_protection = flood_protection + 1
                                    if flood_protection == 5:
                                        time.sleep(5)
                                        flood_protection = 0
                                    db_user = data[i][0]
                                    db_date = data[i][1]
                                    db_mod = data[i][2]
                                    db_version = data[i][3]
                                    db_timeout = data[i][4]
                                    db_num_players = data[i][5]
                                    if ( db_mod.lower() == mod or db_mod.lower() == 'all' ):
                                        if ( re.search(db_version, version) or db_version.lower() == 'all' ):
                                            try:
                                                db_num_players = int(db_num_players)
                                                if db_num_players <= int(players):
                                                    check_num_players = True
                                                else:
                                                    check_num_players = False
                                            except:
                                                check_num_players = True
                                            if ( check_num_players == True ):
                                                check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user)
                                flood_protection = 0
            length = len(notify_ip_list)
            indexes = []
            for i in range(int(length)):
                if ( notify_ip_list[i] not in ip_current_games ):
                    indexes.append(i)   #indexes to remove from notify_ip_list
                else:
                    index_for_players = ip_current_games.index(notify_ip_list[i])
                    notify_players_list[i] = players_current_games[index_for_players]
            for i in indexes:
                del notify_ip_list[i]
                del notify_players_list[i]
