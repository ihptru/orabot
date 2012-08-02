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
Says 'Hello' back
"""

def hi(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 1 ):
        self.send_reply( ("Yo " + user + "! Whats up?"), user, channel )
    else:
        self.send_reply( ("Yo " + user + "! Whats up? And wth is '"+" ".join(command[1:])+"'"), user, channel )
