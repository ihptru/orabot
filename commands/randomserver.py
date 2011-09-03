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

import random

def randomserver(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) >= 4 ):
        if ( command[1][0:2] == '-c' ):
            max_positions = command[1][2:]
            if ( max_positions != '' ):
                try:
                    max_positions = int(max_positions)
                except:
                    self.send_reply( ("Error: `-c` takes only integer value!"), user, channel )
                    return
                if ( max_positions >= 2 ):
                    arguments = command[2:]
                    if ( int(len(arguments)) >= max_positions ):
                        if ( (max_positions == 2) or (max_positions == 4) or (max_positions == 8) or (max_positions == 16) or (max_positions == 32) ):
                            round_list = []
                            output_name = '/var/sites/lv-vl/randomserver/'+time.strftime('%y%m%d%H%M%S',time.localtime())+'.txt'
                            output_file = output_name
                            output_name = output_name.split('randomserver/')[1]
                            result = "http://lv-vl.net/randomserver/"+output_name+"   "
                            result_to_file = ''
                            round_number = 1
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
                                    result_to_file = result_to_file+"RD"+str(round_number)+"-server"+str(i)+"="+chosen+"\n"
                                    round_list.append(chosen)
                                result = result+" |"
                                result_to_file = result_to_file+"\n"
                                arguments = round_list
                                round_list = []
                                max_positions = int(max_positions / 2)
                                round_number = round_number + 1
                            f = open(output_file, 'a')
                            f.write(result_to_file)
                            f.close()
                            self.send_reply( (result), user, channel )
                        else:
                            self.send_reply( ("Error: the positions value must be 2, 4, 8, 16, or 32 !"), user, channel )
                    else:
                        self.send_reply( ("Error: at least "+str(max_positions)+" arguments required!"), user, channel )
                else:
                    self.send_reply( ("Error: positions value must be >= 2 !"), user, channel )
            else:
                self.send_reply( ("Error: `-c` takes a value!"), user, channel )
        else:
            self.send_reply( ("Error: option is incorrect!"), user, channel )
    else:
        self.send_reply( ("Error: Max positions and at least 2 arguments required!"), user, channel )
