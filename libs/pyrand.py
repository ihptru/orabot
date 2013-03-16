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

# This module is to randomize teams for tournament brackets in MediaWiki format
# Important usage note:  no spaces in team names
import re
from sys import stdout, argv
from os import stat
from time import sleep, strftime, gmtime, localtime
import random
import config

output_file = ''

def start(self, user, channel, players):
    name = strftime('%y%m%d%H%M%S',localtime())+'.txt'
    global output_file
    output_file = config.randomteam_dir+name
    rand(self, user, channel, players, name)
    
def o_writter(text):
    f = open(output_file, 'a')
    f.write(text)
    f.close()
def qsortRange(a, b, start, end):
    if end - start + 1 < 32:
        insertionSort(a, start, end)
    else:
        pivotIndex = partition(a, start, end, randint(start, end))
        qsortRange(a, start, pivotIndex - 1)
        qsortRange(a, pivotIndex + 1, end)
    return a

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
            o_writter("| RD1-team0"+str(i+1)+"="+players2[i]+"\n")
            playerList=playerList+str(players2[i])+", "
        else:
            o_writter("| RD1-team"+str(i+1)+"="+players2[i]+"\n")
            if(i is (len(players2)-1)):
                playerList=playerList+str(players2[i])
            else:
                playerList=playerList+str(players2[i])+", "
            
    result = config.randomteam_url+name+"   "+playerList
    self.send_reply( (result), user, channel )
