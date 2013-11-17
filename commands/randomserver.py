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

"""
Randomize servers or maps for single elimination tournaments
"""

import random

def randomserver(self, user, channel):
    command = (self.command).split()
    arguments = command[1:]
    if len(arguments) not in [2, 4, 8, 16, 32]:
        self.send_reply( ("I need 2, 4, 8, 16 or 32 arguments"), user, channel )
        return
    round_list = []
    result = "|"
    round_number = 1
    max_positions = len(arguments)
    while (max_positions != 0 ):
        for i in range(max_positions):
            if ( round_number != 1 ):
                current = i + i
                current_end = i + i + 2
                chosen = random.choice(arguments[current:current_end])
            else:
                chosen = random.choice(arguments)
                arguments.remove(chosen)
            result = result+" "+chosen
            round_list.append(chosen)
        result = result+" |"
        arguments = round_list[:]
        round_list = []
        max_positions = int(max_positions / 2)
        round_number = round_number + 1
    self.send_reply( (result), user, channel )
