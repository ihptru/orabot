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

import math

def help(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        self.send_reply( ("Help: https://github.com/ihptru/orabot/wiki"), user, channel )
    else:
        if ( command[1] == 'calc' ):
            if ( len(command) == 3 ):
                function = command[2]
                available = vars(math).keys()
                if ( function in available ):
                    desc = eval("math."+function).__doc__.replace('\n',' ')
                    self.send_reply( (desc), user, channel )
                else:
                    self.send_reply( ("I don't know about '"+function+"'"), user, channel )
            else:
                self.send_reply( ("]calc to make calculations"), user, channel )
        else:
            self.send_reply( ("I don't know anything about '"+" ".join(command[1:])+"'"), user, channel )
