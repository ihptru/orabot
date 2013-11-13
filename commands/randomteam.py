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
Single elimination tournament brackets generator
"""
from time import strftime, localtime
import random

def randomteam(self, user, channel):
    command = (self.command).split()
    if ( len(command) > 3 ):
        name = strftime('%y%m%d%H%M%S',localtime())+'.txt'
        rand(self, user, channel, command[1:], name)
    else:
        self.send_reply( ("You must specify at least 3 teams"), user, channel )

def rand(self, user, channel, players, name):
    teams32=[1,32,17,16,9,24,25,8,5,28,21,12,13,20,29,4,3,30,19,14,11,22,27,6,7,26,23,10,15,18,31,2]
    teams16=[1,15,11,7,5,9,13,3,4,14,10,6,8,12,16,2]
    teams8=[1,7,5,3,4,6,8,2]
    teams4=[1,4,3,2]

    numTeams=len(players)

    for i in range(0,len(players)):
        x = random.randint(i,(len(players)-1))
        temp = players[i]
        players[i] = players[x]
        players[x] = temp
    
    for i in range(0,len(players)):
        x = random.randint(i,(len(players)-1))
        temp = players[i]
        players[i] = players[x]
        players[x] = temp
    byenum=1
    if (numTeams<=4 and numTeams>0):
        teams=teams4
        while (numTeams<4):
            players.append("~bye~"+str(byenum))
            byenum=byenum+1
            numTeams=len(players)
    elif (numTeams<=8 and numTeams>4):
        teams=teams8
        while (numTeams<8):
            players.append("~bye~"+str(byenum))
            byenum=byenum+1
            numTeams=len(players)
    elif (numTeams<=16 and numTeams>8):
        teams=teams16
        while (numTeams<16):
            players.append("~bye~"+str(byenum))
            byenum=byenum+1
            numTeams=len(players)
    elif (numTeams<=32 and numTeams>16):
        teams=teams32
        while (numTeams<32):
            players.append("~bye~"+str(byenum))
            byenum=byenum+1
            numTeams=len(players)
    else:
        self.send_reply( ('I support 32 teams max!'), user, channel )
        return

    players2=[]
    for i in range(0,numTeams):
        players2.append(" ")
    i=0
    for indexVal in teams:
        players2.pop(indexVal-1)
        players2.insert(indexVal-1, players[i])
        i=i+1
    playerList=""
    for i in range(0,len(players2)):
        if (i <9):
            playerList=playerList+str(players2[i])+", "
        else:
            if(i is (len(players2)-1)):
                playerList=playerList+str(players2[i])
            else:
                playerList=playerList+str(players2[i])+", "
    self.send_reply( (playerList), user, channel )
