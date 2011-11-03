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

"""
Shows last release and playtest versions of OpenRA
"""

import time
import re

def version(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 1 ):
        url = 'http://github.com/api/v2/json/repos/show/OpenRA/OpenRA/tags'
        stream = self.data_from_url(url, None)
        
        release = get_version(self, stream, 'release')
        playtest = get_version(self, stream, 'playtest')
        
        if ( int(release.split('.')[0]) < int(playtest.split('.')[0]) ):
            newer = 'playtest is newer then release'
        else:
            newer = 'release is newer then playtest'
        self.send_reply( ("Latest release: "+release[0:4]+" "+release[4:8]+"  | Latest playtest: "+playtest[0:4]+" "+playtest[4:8]+"  | "+newer), user, channel )
        self.send_notice("Release:", user)
        self.send_notice("\twin: http://openra.res0l.net/assets/downloads/windows/OpenRA-release-"+release+".exe", user)
        self.send_notice("\tosx: http://openra.res0l.net/assets/downloads/mac/OpenRA-release-"+release+".zip", user)
        self.send_notice("\tlinux deb: http://openra.res0l.net/assets/downloads/linux/deb/openra_release."+release+"_all.deb", user)
        self.send_notice("\tlinux rpm: http://openra.res0l.net/assets/downloads/linux/rpm/openra-release."+release+"-1.noarch.rpm", user)
        self.send_notice("\tlinux arch(tar.xz): http://openra.res0l.net/assets/downloads/linux/arch/openra-release."+release+"-1-any.pkg.tar.xz", user)
        time.sleep(6)
        self.send_notice("Playtest:", user)
        self.send_notice("\twin: http://openra.res0l.net/assets/downloads/windows/OpenRA-playtest-"+playtest+".exe", user)
        self.send_notice("\tosx: http://openra.res0l.net/assets/downloads/mac/OpenRA-playtest-"+playtest+".zip", user)
        self.send_notice("\tlinux deb: http://openra.res0l.net/assets/downloads/linux/deb/openra_playtest."+playtest+"_all.deb", user)
        self.send_notice("\tlinux rpm: http://openra.res0l.net/assets/downloads/linux/rpm/openra-playtest."+playtest+"-1.noarch.rpm", user)
        self.send_notice("\tlinux arch(tar.xz): http://openra.res0l.net/assets/downloads/linux/arch/openra-playtest."+playtest+"-1-any.pkg.tar.xz", user)
    else:
        self.send_reply( ("Error, wrong request"), user, channel )

def get_version(self, stream, version):
    version = re.findall('.*?"'+version+'-(.*?)"', stream)
    version.sort()
    return version[-1]
