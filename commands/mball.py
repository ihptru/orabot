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

"""
Tells you what your future is.
Shuffles the answers list and then randomly picks one
"""

import random

def mball(self, user, channel):
    command = (self.command).split()
    if ( len(command) > 3 ):
        answers = ['It is certain', 'It is decidedly so', 'Without a doubt', \
                'Yes - definitely', 'You may rely on it', 'As I see it, yes',\
                'Most likely', 'Outlook good', 'Signs point to yes', 'Yes', \
                'Reply hazy, try again', 'Ask again later', 'Better not tell you now', \
                'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', \
                'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful', \
                ]
        self.send_reply( (random.choice(answers)), user, channel)
    else:
        self.send_notice( ('error, at least 3 arguments required'), user )
