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

import urllib.request

def version(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        url = 'http://openra.res0l.net/download/linux/deb/index.php'
        stream = urllib.request.urlopen(url).read().decode('utf-8')
        release = stream.split('<ul')[1].split('<li>')[1].split('>')[1].split('</a')[0]
        playtest = stream.split('<ul')[2].split('<li>')[1].split('>')[1].split('</a')[0]
        if ( int(release.split('.')[0]) < int(playtest.split('.')[0]) ):
            newer = 'playtest is newer then release'
        else:
            newer = 'release is newer then playtest'
        self.send_reply( ("Latest release: "+release[0:4]+""+release[4:8]+" | Latest playtest: "+playtest[0:4]+""+playtest[4:8]+" | "+newer), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
