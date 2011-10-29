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
import re
import sqlite3
import urllib.request

def start(self):
    conn, cur = self.db_data()
    sql = """DELETE FROM commits
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
    
    def update_commits(self, titles, repo, branch):
        conn, cur = self.db_data()
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
    
    repos = self.git_repos.split()
    if ( len(repos) == 0 ):
        return  #no repositories specified
    print("Updating commits table...")
    for repo in repos:
        if ( repo[-1] == '/' ):
            slash = ''
        else:
            slash = '/'
        repo = repo + slash
        branches = branch_list(self, repo)
        if ( len(branches) == 0 ):
            print("Error fetching list of branches from repo: " + repo)
        else:
            for branch in branches:
                url = repo + branch
                titles = get_commits(self, url)
                if ( len(titles) == 0 ):
                    print("### Something went wrong fetching commits info! ###")
                    conn, cur = self.db_data()
                    sql = """DELETE FROM commits
                            WHERE repo = '"""+repo+"""' AND branch = '"""+branch+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    cur.close()
                else:
                    update_commits(self, titles, repo, branch)
    print("Updating commits table completed!")
    
    while True:
        time.sleep(60)
        detect_commits(self)

def detect_commits(self):
    flood_protection = 0
    repos = self.git_repos.split()
    for repo in repos:
        if ( repo[-1] == '/' ):
            slash = ''
        else:
            slash = '/'
        repo = repo + slash
        branches = branch_list(self, repo)
        if ( len(branches) == 0 ):
            print("Error fetching list of branches from repo: " + repo)
            return
        for branch in branches:
            url = repo + branch
            conn, cur = self.db_data()
            sql = """SELECT title FROM commits
                    WHERE repo = '"""+repo+"""' AND branch = '"""+branch+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            titles = get_commits(self, url)
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
                for channel in self.write_commit_notifications_to.split():
                    commit = self.parse_html(commits_to_show[i])
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

def branch_list(self, repo):
    repo = 'http://github.com/api/v2/json/repos/show' + repo.split('https://github.com')[1] + 'branches'
    try:
        stream = self.data_from_url(repo, None)
    except Exception as e:
        print(e)
        return []
    branches = re.findall('"(.*?)":".*?"',stream[12:-1])
    return branches

def get_commits(self, url):   #this functions must get url of Branch
    url = 'http://github.com/api/v2/json/commits/list' + url.split('https://github.com')[1]
    titles = []
    try:
        stream = self.data_from_url(url, None)
    except Exception as e:
        print(e)
        return titles
    titles = re.findall('.*?"message":"(.*?)"',stream)
    return titles
