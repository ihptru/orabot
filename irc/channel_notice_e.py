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

# Module for channel NOTICE event

def parse_event(self, recv):
    nick = recv.split(':')[1].split('!')[0]
    message = recv[recv.find(" :")+2:]
    chan = recv.split()[2]
    self.logs(nick, chan, 'channel_notice', message, '')
    print ( ( "[%s NOTICE to %s] %s: %s" ) % (self.irc_host, chan, nick, message) )
