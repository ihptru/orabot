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

import config
import re

show_possible=['games', 'help', 'version', 'hi', 'randomteam', 'tr', 'lang', 'last', 'online', 'weather', 'lastgame', 'who', 'promote', 'maps', 'say','mapinfo','calc','faq']

def show(self, user, channel):
    if self.OpVoice(user, channel):
        command = (self.command)
        command = command.split()
        if ( len(command) >= 4 ):
            if ( command[-2] == '|' ):
                to_user = command[-1]
                if (( to_user[0] == '#' ) or ( to_user[0] == ',' )):
                    self.send_reply( ("Impossible to redirect output to channel!"), user, channel )
                    return
                if re.search("^#", channel):
                    #send NAMES channel to server
                    str_buff = ( "NAMES %s \r\n" ) % (channel)
                    self.irc_sock.send (str_buff.encode())
                    #recover all nicks on channel
                    recv = self.irc_sock.recv( 4096 )

                    if str(recv).find ( " 353 "+config.bot_nick ) != -1:
                        user_nicks = str(recv).split(':')[2].rstrip()
                        user_nicks = user_nicks.replace('+','').replace('@','').replace('%','')
                        user_nicks = user_nicks.split(' ')

                    if ( to_user not in user_nicks ):  #reciever is NOT on the channel
                        self.send_message_to_channel( (user+", I can not send an output of this command to user which is not on the channel!"), channel)
                        return
                show_command = command[1:-2]
                show_command = " ".join(show_command)
                show_command = show_command.replace(']','')
                show_command = show_command.split()
                if ( show_command[0] in show_possible ):
                    self.command = " ".join(show_command)
                    eval (show_command[0]+'.'+show_command[0])(self, to_user, to_user)
                else:
                    self.send_reply( ("I can not show output of this command to user"), user, channel )
            else:
                self.send_reply( ("Syntax error"), user, channel )
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
    else:
        self.send_reply( ("Nice try!"), user, channel )
