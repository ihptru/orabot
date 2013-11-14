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

import imp
import os
import re
import signal
import inspect

_commands = os.listdir('commands')

def module_check(item):
    if re.search('^\.', item):
        return False
    if re.search('pyc$', item):
        return False
    if re.search('__init__.py', item):
        return False
    if re.search('__pycache__', item):
        return False
    return True

for item in _commands:
    if not module_check(item):
        continue
    exec("from commands import " + item.split('.py')[0])

# Execute command
def evalCommand(self, commandname, user, channel):
    try:
        imp.find_module('commands/'+commandname)
    except:
        return  # no such command
    imp.reload(eval(commandname))
    command_function = getattr(eval(commandname), commandname, None)
    if command_function != None:
        if inspect.isfunction(command_function):

            class TimedOut(Exception): # Raised if timed out.
                pass

            def signal_handler(signum, frame):
                raise TimedOut("Timed out!")

            signal.signal(signal.SIGALRM, signal_handler)

            signal.alarm(self.command_timeout)    # Limit command execution time
            try:
                command_function(self, user, channel)
                signal.alarm(0)
            except TimedOut:
                self.send_reply( ("Timed out!"), user, channel)
