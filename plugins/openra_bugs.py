# Copyright 2011-2012 orabot Developers
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
    conn, cur = self.db_data()
    sql = """SELECT num FROM bugs
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    
    e_bugs = [int(rec[0]) for rec in records]   # existing bugs in DB
    
    y = bugs_list(self) # new list from a remote server
    
    remote_bugs = [n['number'] for n in y['issues']]
    remote_titles = [t['title'] for t in y['issues']]

    for bug in remote_bugs:
        if bug not in e_bugs:   # remote bug is not found in existing bugs
            sql = """INSERT INTO bugs
                    (title,num)
                    VALUES
                    (
                    '{0}',
                    '{1}'
                    )
            """.format(y['issues'][remote_bugs.index(bug)]['title'].replace("'", "\\'"), bug)
            cur.execute(sql)
            conn.commit()
            e_bugs.append(bug)
    
    while True:
        time.sleep(120)
        e_bugs = detect_bugs(self, conn, cur, e_bugs)

def detect_bugs(self, conn, cur, e_bugs):
    y = bugs_list(self)
    remote_bugs = [n['number'] for n in y['issues']]
    remote_titles = [t['title'] for t in y['issues']]
    
    for bug in remote_bugs:
        if bug not in e_bugs:   # it's a new bug
            sql = """INSERT INTO bugs
                    (title,num)
                    VALUES
                    (
                    '{0}',
                    '{1}',
                    )
            """.format(y['issues'][remote_bugs.index(bug)]['title'].replace("'", "\\'"), bug)
            cur.execute(sql)
            conn.commit()
            e_bugs.append(bug)
            self.send_message_to_channel( ("New issue #" + bug + " by " + y['issues'][remote_bugs.index(bug)]['user'] + ": " + y['issues'][remote_bugs.index(bug)]['title'] + " | " + y['issues'][remote_bugs.index(bug)]['html_url']), self.write_bug_notifications_to.split()[0] )

    return e_bugs

def bugs_list(self):
    url = 'http://github.com/api/v2/json/issues/list/OpenRA/OpenRA/open'
    try:
        data = urllib.request.urlopen(url).read().decode()
        return json.loads(data)
    except:
        time.sleep(900)
        bugs_list(self)
