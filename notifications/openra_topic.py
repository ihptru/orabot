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
    while  True:
        time.sleep(120)
        change_topic(self)

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
