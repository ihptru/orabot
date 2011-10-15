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
import config
import urllib.request

def start(self):
    while True:
        time.sleep(120)
        bugreport(self)

def bugreport(self):
    url = 'http://bugs.open-ra.org/projects/openra/issues.atom'
    try:
        stream = self.data_from_url(url, None)
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
        bug_report_title = self.parse_html(bug_report_title)
        message = bug_report_title+" | "+bug_report_url
        for channel in config.write_bug_notifications_to.split(','):
            self.send_message_to_channel( (message), channel )
