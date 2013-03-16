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
import urllib.request
import json

def start(self):
    time.sleep(1800)    # wait 30 minutes
    conn, cur = self.db_data()
    sql = """SELECT num FROM bugs
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    
    e_bugs = [int(rec[0]) for rec in records]   # existing bugs in DB
    
    y = bugs_list(self) # new list from a remote server
    
    remote_bugs = [n['number'] for n in y]
    remote_titles = [t['title'] for t in y]

    for bug in remote_bugs:
        if bug not in e_bugs:   # remote bug is not found in existing bugs, then update table
            sql = """INSERT INTO bugs
                    (title,num)
                    VALUES
                    (
                    '{0}',
                    '{1}'
                    )
            """.format(y[remote_bugs.index(bug)]['title'].replace("'", "''"), bug)
            cur.execute(sql)
            conn.commit()
            e_bugs.append(bug)
    
    while True:
        time.sleep(1200)    # wait 20 minutes
        e_bugs = detect_bugs(self, conn, cur, e_bugs)

def detect_bugs(self, conn, cur, e_bugs):
    y = bugs_list(self)
    remote_bugs = [n['number'] for n in y]
    remote_titles = [t['title'] for t in y]
    
    for bug in remote_bugs:
        if bug not in e_bugs:   # it's a new bug
            sql = """INSERT INTO bugs
                    (title,num)
                    VALUES
                    (
                    '{0}',
                    '{1}'
                    )
            """.format(y[remote_bugs.index(bug)]['title'].replace("'", "''"), bug)
            cur.execute(sql)
            conn.commit()
            e_bugs.append(bug)
            self.send_message_to_channel( ("New issue #" + str(bug) + " by " + y[remote_bugs.index(bug)]['user']['login'] + ": " + y[remote_bugs.index(bug)]['title'] + " | http://bugs.open-ra.org/" + str(bug)), self.write_bug_notifications_to.split()[0] )

    return e_bugs

def bugs_list(self):
    url = 'https://api.github.com/repos/OpenRA/OpenRA/issues'
    while 1:
        try:
            data = urllib.request.urlopen(url).read().decode()
            return json.loads(data)
        except:
            print("*** Error: could not fetch a list of OpenRA bugs *** Probably Exceed Rate Limit")
            time.sleep(7200)    # wait 2 hours
