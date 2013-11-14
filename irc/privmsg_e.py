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

# Module for PRIVMSG event

import re

def parse_event(self, irc_user_nick, irc_user_message, chan):    
    action = re.findall('^ACTION (.*?)$', irc_user_message)
    if ( len(action) != 0 ):
        self.logs(irc_user_nick, chan, 'action', action[0], '')
    else:
        self.logs(irc_user_nick, chan, 'privmsg', irc_user_message, '')
    # logs end
    print ( ( "[%s %s] %s: %s" ) % (self.irc_host, chan, irc_user_nick, irc_user_message) )
    # Message starts with command prefix?
    if ( irc_user_message != '' ):
        if ( irc_user_message[0] == self.command_prefix ):
            self.command = irc_user_message[1:].replace("'","''")
            self.process_command(irc_user_nick.lower(), chan)
    self.spam_filter(irc_user_nick.lower(), chan)
    # parse links and bug reports numbers
    self.parse_link(chan, irc_user_nick.lower(), irc_user_message)
    self.parse_bug_num(chan, irc_user_message)
