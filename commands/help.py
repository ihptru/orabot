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
import inspect

___all___ = ["games","add","adduser","calc","faq","hi","ifuser","lang","last","lastgame","later","mapinfo","maps","notify","promote","randomserver","randomteam","remove","unnotify","version","weather","who","complain","join","log","part","pickup_remove","quit","say","show","subscribed","unsubscribe","pingme","uptime"]

for item in ___all___:
    exec("from commands import " + item)

def help(self, user, channel):
    command = (self.command)
    command = command.split()
    no_desc = "No description available"
    help_desc = "(help [<command module>] [<command>]) -- This command gives a useful description of what <command module> does. <command> is only necessary if the command module contains commands tree. (help commands) -- gives a list of commands"
    if ( len(command) == 1 ):
        self.send_reply( (help_desc), user, channel )
    elif ( len(command) == 2 ):
        if ( command[1] == "help" ):
            self.send_reply( (help_desc), user, channel )
            return
        if ( command[1] == 'commands' ):
            self.send_notice( ("Commands: help " + " ".join(___all___)), user )
            return
        if ( command[1] in ___all___ ):
            desc = eval(command[1]).__doc__
            if ( desc != None ):
                desc = desc.strip().replace('\n', ' ')
                if ( len(desc) != 0 ):
                    self.send_reply( (desc), user, channel )
                else:
                    self.send_reply( (no_desc), user, channel)
            else:
                self.send_reply( (no_desc), user, channel)
        else:
            self.send_reply( ("Error: There is no command module: " + command[1]), user, channel )
    elif ( len(command) == 3 ):
        module = command[1]
        function = command[2]
        if ( command[1] == 'calc' ):
            available = vars(math).keys()
            if ( function in available ):
                desc = eval("math."+function).__doc__
                self.send_reply( (desc.replace('\n', ' ')), user, channel )
            else:
                self.send_reply( (no_desc), user, channel )
            return
        if ( module in ___all___ ):
            function = getattr(eval(module), function, None)
            if ( function != None ):
                if ( inspect.isfunction(function) ):
                    desc = function.__doc__
                    if ( desc != None ):
                        desc = desc.strip().replace('\n', ' ')
                        if ( len(desc) != 0 ):
                            self.send_reply( (desc), user, channel )
                        else:
                            self.send_reply( (no_desc), user, channel)
                    else:
                        self.send_reply( (no_desc), user, channel)
                else:
                    self.send_reply( ("Error: no such command in command module"), user, channel)
            else:
                self.send_reply( ("Error: no such command in command module"), user, channel)
        else:
            self.send_reply( ("Error: nothing found"), user, channel)
    else:
        self.send_reply( ("Syntax Error!"), user, channel)
