# Copyright 2011-2014 orabot Developers
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

def start(self):
    if self.irc_host != "irc.freenode.net":
        print("*** [%s] Terminating child process (unsupported): %s" % (self.irc_host, __name__))
        return
    servers_to_test = {}
    servers_to_test['mirrors'] = {}
    servers_to_test['servers'] = {}
    servers_to_test['servers']['http://master.open-ra.org/list.php'] = 0
    servers_to_test['servers']['http://openra.net'] = 0
    servers_to_test['servers']['http://resource.openra.net'] = 0

    reconf_mirror_list = 0

    while True:
        time.sleep(600)    # wait 10 minutes

        if reconf_mirror_list == 0:
            try:
                data = urllib.request.urlopen('http://www.openra.net/packages/ra-mirrors.txt').read().decode()
                for s1 in data.split():
                    servers_to_test['mirrors'][s1] = 0
            except:
                pass

        servers_to_test = check_servers(self, servers_to_test)
        reconf_mirror_list += 1
        if reconf_mirror_list >= 100:
            reconf_mirror_list = 0

def check_servers(self, servers_to_test):
    for item in servers_to_test:
        for server in servers_to_test[item]:
            try:
                data = urllib.request.urlopen(server).read(1)
                if servers_to_test[item][server] != 0:
                    servers_to_test[item][server] = 0
            except:
                if servers_to_test[item][server] >= 10:
                    servers_to_test[item][server] = 0
                if servers_to_test[item][server] == 0:
                    self.send_message_to_channel('4Alert! 3%s 4is unreachable!' % server, "#openra")
                servers_to_test[item][server] += 1
    return servers_to_test