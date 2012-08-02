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

"""
Use this to make bot leave a particular channel
"""

def part(self, user, channel):
    if not self.Admin(user, channel):
        return
    command = (self.command).split()
    if ( len(command) == 2 ):
        if ( (command[1])[0] == "#"):
            irc_channel = command[1]
        else:
            irc_channel = "#" + command[1]
        self.quit_channel(irc_channel)
