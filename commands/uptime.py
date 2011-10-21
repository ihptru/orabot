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
Computes the uptime of the bot
"""

import time
import datetime

def uptime(self, user, channel):
    if not self.OpVoice(user, channel):
        return
    command = (self.command).split()
    if ( len(command) == 1 ):
        current = time.mktime(time.strptime( time.strftime('%Y-%m-%d-%H-%M-%S'), '%Y-%m-%d-%H-%M-%S'))
        difference = current - self.start_time
        result = str(datetime.timedelta(seconds = difference))
        self.send_reply( (result), user, channel)
    else:
        self.send_reply( ("error"), user, channel)
