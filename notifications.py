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
import config
import html.parser

def parse_html(string):
    h = html.parser.HTMLParser()
    string = h.unescape(string)
    return string

def change_topic(self):
    def write_version(release, playtest):
        filename = 'version.txt'
        file = open(filename, 'w')
        file.write(release + "\n" + playtest + "\n")
        file.close()

    url = 'http://openra.res0l.net/download/linux/deb/index.php'
    try:
        stream = urllib.request.urlopen(url).read().decode('utf-8')
    except:
        pass    #can not reach page in 90% cases
    release = stream.split('<ul')[1].split('<li>')[1].split('>')[1].split('</a')[0]
    playtest = stream.split('<ul')[2].split('<li>')[1].split('>')[1].split('</a')[0]
    filename = 'version.txt'
    lines = []
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()
    except:
        pass    #no file exists
    if ( lines == [] ):
        write_version(release, playtest)
        return
    if ( (release + '\n' not in lines) or (playtest + '\n' not in lines) ):
        topic = "open-source RTS | latest: "+release+" | testing: "+playtest+" | http://open-ra.org | bugs: http://bugs.open-ra.org"
        self.topic(config.change_topic_channel, topic)
        print("### DEBUG: made an attempt to change the TOPIC of " + config.change_topic_channel + " ###")
        write_version(release, playtest)

def branch_list(repo):
    repo = 'http://github.com/api/v2/json/repos/show' + repo.split('https://github.com')[1] + 'branches'
    try:
        stream = urllib.request.urlopen(repo).read().decode('utf-8')
    except:
        return []
    branches = re.findall('"(.*?)":".*?"',stream[12:-1])
    return branches
        

def get_commits(url):   #this functions must get url of Branch
    url = 'http://github.com/api/v2/json/commits/list' + url.split('https://github.com')[1]
    titles = []
    try:
        stream = urllib.request.urlopen(url).read().decode('utf-8')
    except:
        return titles
    titles = re.findall('.*?"message":"(.*?)"',stream)
    return titles


def check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn):
    notify_message = "New game: "+name+" - mod: "+mod+version+" - Already "+players+" players in"
    if ( db_timeout.lower() == 'all' ):
        self.send_reply( (notify_message), db_user, db_user )
    elif ( db_timeout.lower() == 'till_quit' ):
        self.send_reply( (notify_message), db_user, db_user )
    elif ( db_timeout.lower() == 'f' or db_timeout.lower() == 'forever' ):
        sql = """SELECT state FROM users
                WHERE user = '"""+db_user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):
            if ( str(records[0][0]) == '1' ):
                self.send_reply( (notify_message), db_user, db_user )
    else:
        date_of_adding_seconds = time.mktime(time.strptime( db_date, '%Y-%m-%d-%H-%M-%S'))
        localtime = time.strftime('%Y-%m-%d-%H-%M-%S')
        localtime = time.mktime(time.strptime( localtime, '%Y-%m-%d-%H-%M-%S'))
        difference = localtime - date_of_adding_seconds     #in result - must be less then timeout
        if ( db_timeout[-1] == 's' ):
            timeout = db_timeout[0:-1]
        elif ( db_timeout[-1] == 'm' ):
            timeout = int(db_timeout[0:-1]) * 60
        elif ( db_timeout[-1] == 'h' ):
            timeout = int(db_timeout[0:-1]) * 3600
        elif ( db_timeout[-1] == 'd' ):
            timeout = int(db_timeout[0:-1]) * 86400
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
    topic_var = 0

    conn = sqlite3.connect('../db/openra.sqlite')
    cur = conn.cursor()
    sql = """DELETE FROM commits
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
    
    def update_commits(titles, repo, branch):
        conn = sqlite3.connect('../db/openra.sqlite')
        cur = conn.cursor()
        sql = """DELETE FROM commits
                WHERE repo = '"""+repo+"""' AND branch = '"""+branch+"""'
        """
        cur.execute(sql)
        conn.commit()
        for i in range(len(titles)):
            sql = """INSERT INTO commits
                    (title,repo,branch)
                    VALUES
                    (
                    '"""+titles[i].replace("'","''")+"""','"""+repo+"""','"""+branch+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
        cur.close()
        print("Updating commits table...")

    repos = config.git_repos.split()
    for repo in repos:
        if ( repo[-1] == '/' ):
            slash = ''
        else:
            slash = '/'
        repo = repo + slash
        branches = branch_list(repo)
        if ( len(branches) == 0 ):
            print("Error fetching list of branches from repo: " + repo)
        else:
            for branch in branches:
                url = repo + branch
                titles = get_commits(url)
                if ( len(titles) == 0 ):
                    print("### Something went wrong fetching commits info! ###")
                    conn = sqlite3.connect('../db/openra.sqlite')
                    cur = conn.cursor()
                    sql = """DELETE FROM commits
                            WHERE repo = '"""+repo+"""' AND branch = '"""+branch+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    cur.close()
                else:
                    update_commits(titles, repo, branch)
    print("Updating commits table completed!")

    while True:
        time.sleep(5)
        bugreport_var = bugreport_var + 1
        commit_var = commit_var + 1
        topic_var = topic_var + 1
        ###change topic
        if ( topic_var == 30 ):
            topic_var = 0
            change_topic(self)
        ### commits
        if ( commit_var == 30 ):
            commit_var = 0
            def commits(self):
                flood_protection = 0
                repos = config.git_repos.split()
                for repo in repos:
                    if ( repo[-1] == '/' ):
                        slash = ''
                    else:
                        slash = '/'
                    repo = repo + slash
                    branches = branch_list(repo)
                    if ( len(branches) == 0 ):
                        print("Error fetching list of branches from repo: " + repo)
                        return
                    for branch in branches:
                        url = repo + branch
                        conn = sqlite3.connect('../db/openra.sqlite')
                        cur = conn.cursor()
                        sql = """SELECT title FROM commits
                                WHERE repo = '"""+repo+"""' AND branch = '"""+branch+"""'
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        titles = get_commits(url)
                        if ( len(titles) == 0 ):
                            print("### Something went wrong fetching commits info! ###")
                            return
                        if ( len(records) == 0 ):   #There was an error at notification's start (probably fetching error(caused by socket)), so `commits` table is clear
                            ### current fetch is full of commits, so we fill table; return; do not notify
                            for i in range(len(titles)):
                                sql = """INSERT INTO commits
                                        (title,repo,branch)
                                        VALUES
                                        (
                                        '"""+titles[i].replace("'","''")+"""','"""+repo+"""','"""+branch+"""'
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
                                # commit title is not in list of commits, related to current branch, but this can be merge
                                # so we should not spam and notify of commit which was already seen in different branch
                                sql = """SELECT title FROM commits
                                        WHERE title = '"""+titles[i].replace("'","''")+"""'
                                """
                                cur.execute(sql)
                                records = cur.fetchall()
                                conn.commit()
                                if ( len(records) == 0 ):   # no same commit's name found in 'commits' table
                                    commits_to_show.append(titles[i])
                        commits_to_show.reverse()
                        for i in range(len(commits_to_show)):
                            flood_protection = flood_protection + 1
                            if flood_protection == 5:
                                time.sleep(5)
                                flood_protection = 0
                            for channel in config.write_commit_notifications_to.split(','):
                                commit = parse_html(commits_to_show[i])
                                self.send_message_to_channel( ("News from "+repo.split('github.com/')[1]+branch+": "+commit), channel )
                            sql = """INSERT INTO commits
                                    (title,repo,branch)
                                    VALUES
                                    (
                                    '"""+commits_to_show[i].replace("'","''")+"""','"""+repo+"""','"""+branch+"""'
                                    )
                            """
                            cur.execute(sql)
                            conn.commit()
                        flood_protection = 0
                        cur.close()
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
                    bug_report_title = parse_html(bug_report_title)
                    message = bug_report_title+" | "+bug_report_url
                    for channel in config.write_bug_notifications_to.split(','):
                        self.send_message_to_channel( (message), channel )
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
                        conn = sqlite3.connect('../db/openra.sqlite')
                        cur = conn.cursor()
                        sql = """INSERT INTO games
                                (game,players,date_time,version)
                                VALUES
                                (
                                '"""+name.replace("'","''")+"""','"""+players+"""',strftime('%Y-%m-%d-%H-%M-%S'),'"""+version+"""'
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                        cur.close()
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
                                                check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn)
                                flood_protection = 0
                            cur.close()
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
                                                check_timeout_send(self, name, mod, version, players, db_timeout, db_date, db_user, cur, conn)
                                flood_protection = 0
                            cur.close()
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
