# Copyright 2011-2016 orabot Developers
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

def start(self):
    if self.irc_host != "irc.openra.net":
        print("*** [%s] Terminating child process (unsupported): %s" % (self.irc_host, __name__))
        return

    while  True:
        time.sleep(1800)  # wait 30 minutes
        push_ads(self)

def push_ads(self):
    self.send_message_to_channel('Join our Tag Team Tournament - March 5th/6th -12th/13th Cash prizes See http://forum.openra.net/82/19414/ For details', '#lobby')