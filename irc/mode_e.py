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

def parse_event(self, recv):
    who_gives = recv.split('!')[0][1:]
    user = recv.split()[4]
    channel = recv.split()[2]
    option = recv.split()[3]
    
    self.send_names(channel)
    
    if ( option == '+o' ):
        row = who_gives + " gives channel operator status to " + user
    elif ( option == '-o' ):
        row = who_gives + " removes channel operator status from " + user
    elif ( option == '+v' ):
        row = who_gives + " gives voice to " + user
    elif ( option == '-v' ):
        row = who_gives + " removes voice from " + user
    elif ( option == '+h' ):
        row = who_gives + " gives halfop to " + user
    elif ( option == '-h' ):
        row = who_gives + " removes halfop from " + user
    
    self.logs('', channel, 'mode', row, '')
    
