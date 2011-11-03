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

def start(self):
    while  True:
        time.sleep(120)
        change_topic(self)

def change_topic(self):
    def write_version(release, playtest):
        filename = 'var/version.txt'
        file = open(filename, 'w')
        file.write(release + "\n" + playtest + "\n")
        file.close()

    url = 'http://github.com/api/v2/json/repos/show/OpenRA/OpenRA/tags'
    try:
        stream = self.data_from_url(url, None)
    except Exception as e:
        print(e) #can not reach page in 90% cases
        return
    release = get_version(self, stream, 'release')
    playtest = get_version(self, stream, 'playtest')
    filename = 'var/version.txt'
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
        if ( self.change_topic_channel == '' ):
            return
        topic = "open-source RTS | latest: "+release+" | testing: "+playtest+" | http://open-ra.org | bugs: http://bugs.open-ra.org"
        self.topic(self.change_topic_channel, topic)
        print("[%s] ### DEBUG: made an attempt to change the TOPIC of " + self.change_topic_channel + " ###" % self.irc_host)
        write_version(release, playtest)

def get_version(self, stream, version):
    version = re.findall('.*?"'+version+'-(.*?)"', stream)
    version.sort()
    return version[-1]
