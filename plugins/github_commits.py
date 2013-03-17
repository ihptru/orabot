# Copyright 2011-2013 orabot Developers
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
import urllib.request

def start(self):
    time.sleep(1800)    # wait 30 minutes
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
    if ( self.write_commit_notifications_to == '' ):
        return  #no place where to write commit notifications
    print("[%s] Updating commits table..." % self.irc_host)
    for repo in repos:
        if ( repo[-1] == '/' ):
            slash = ''
        else:
            slash = '/'
        repo = repo + slash
        branches = branch_list(self, repo)
        if ( len(branches) == 0 ):
            print(("[%s] Error fetching list of branches from repo: " + repo) % (self.irc_host))
        else:
            for branch in branches:
                titles = get_commits(self, branch, repo)
                if ( len(titles) == 0 ):    #could not get commits, clear related records from DB just in case... we'll update it later in program flow
                    print(("[%s] ### Something went wrong fetching commits info! ###") % (self.irc_host))
                    conn, cur = self.db_data()
                    sql = """DELETE FROM commits
                            WHERE repo = '"""+repo+"""' AND branch = '"""+branch+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    cur.close()
                else:
                    update_commits(self, titles, repo, branch)
    print(("[%s] Updating commits table completed!") % (self.irc_host))
    
    while True:
        time.sleep(1200)    # wait 20 minutes
        detect_commits(self)

def detect_commits(self):
    repos = self.git_repos.split()
    for repo in repos:
        if ( repo[-1] == '/' ):
            slash = ''
        else:
            slash = '/'
        repo = repo + slash
        branches = branch_list(self, repo)
        if ( len(branches) == 0 ):
            print(("[%s] Error fetching list of branches from repo: " + repo) % (self.irc_host))
            return
        for branch in branches:
            conn, cur = self.db_data()
            sql = """SELECT title FROM commits
                    WHERE repo = '"""+repo+"""' AND branch = '"""+branch+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            titles = get_commits(self, branch, repo)
            if ( len(titles) == 0 ):
                print(("[%s] ### Something went wrong fetching commits info! ###") % (self.irc_host))
                return
            if ( len(records) == 0 ):   #There was an error at notification's start (probably fetching error(caused by socket)), so `commits` table is clear
                # current fetch is full of commits, so we fill table; return; do not notify
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
                    # commit's title is not in list of commits, related to current branch, but there is a possibility this can be merge
                    # so we should not spam and notify of commit which was already seen in different branch, checking it now:
                    sql = """SELECT title FROM commits
                            WHERE title = '"""+titles[i].replace("'","''")+"""'
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    if ( len(records) == 0 ):   # no same commit's name found in 'commits' table, should notify then
                        commits_to_show.append(titles[i])
            commits_to_show.reverse()
            for i in range(len(commits_to_show)):
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
            cur.close()

def branch_list(self, repo):
    repo = 'https://api.github.com/repos' + repo.split('https://github.com')[1] + 'branches'
    while 1:
        try:
            stream = self.data_from_url(repo, None)
            branches = re.findall('.*?"name":"(.*?)"',stream)
            return branches
        except Exception as e:
            print(e+"  ===  Probably Exceed Rate Limit (branch_list function)")
            time.sleep(7200)    # wait 2 hours

def get_commits(self, branch, repo):   #this functions must receive branch name (returns the latest commit for a branch
    url = 'https://api.github.com/repos' + repo.split('https://github.com')[1] + 'commits/' + branch
    while 1:
        try:
            stream = self.data_from_url(url, None)
            titles = re.findall('.*?"message":"(.*?)"',stream)
            return titles
        except Exception as e:
            print(e+"  ===  Probably Exceed Rate Limit (get_commits function)")
            time.sleep(7200)    # wait 2 hours
