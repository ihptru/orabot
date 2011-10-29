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
Redirect of specified command's output to specified user
"""

import re
import time
import os

_commands = os.listdir('commands')
___all___ = []

def module_check(item):
    if re.search('^\.', item):
        return False
    if re.search('pyc$', item):
        return False
    if re.search('__init__.py', item):
        return False
    if re.search('help\..*', item):
        return False
    if re.search('show\..*', item):
        return False
    return True

for item in _commands:
    if not module_check(item):
        continue
    item = item.split('.py')[0]
    ___all___.append(item)
    exec("from commands import " + item)

def show(self, user, channel):
    if not self.Admin(user, channel):
        return
    command = (self.command).split()
    if ( len(command) >= 4 ):
        if ( command[-2] == '|' ):
            to_user = command[-1]
            if (( to_user[0] == '#' ) or ( to_user[0] == ',' )):
                self.send_reply( ("Impossible to redirect output to channel!"), user, channel )
                return
            if not re.search("^#", channel):
                message = "Command can be used only on a channel..."
                self.send_notice( message, user )
                return
            show_command = command[1:-2]
            show_command = " ".join(show_command)
            show_command = show_command.replace(']','')
            show_command = show_command.split()
            if ( show_command[0] in ___all___ ):
                self.command = " ".join(show_command)
                eval (show_command[0]+'.'+show_command[0])(self, to_user, to_user)
            else:
                self.send_reply( ("I can not show output of this command to user"), user, channel )
        else:
            self.send_reply( ("Syntax error"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
