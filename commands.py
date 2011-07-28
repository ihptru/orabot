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

import os
import re
from datetime import date
import sqlite3
import hashlib
import random
import pywapi
import urllib.request
import time
import math
from math import *

import pyrand

languages=['af','sq','ar','be','bg','ca','zh-CN','hr','cs','da','nl','en','et','tl','fi','fr','gl','de','el','iw','hi','hu','is','id','ga','it','ja','ko','lv','lt','mk','ml','mt','no','fa','pl','ro','ru','sr','sk','sl','es','sw','sv','th','tr','uk','vi','cy','yi']
real_langs=['Afrikaans','Albanian','Arabic','Belarusian','Bulgarian','Catalan','Chinese_Simplified','Croatian','Czech','Danish','Dutch','English','Estonian','Filipino','Finnish','French','Galician','German','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Irish','Italian','Japanese','Korean','Latvian','Lithuanian','Macedonian','Malay','Maltese','Norwegian','Persian','Polish','Romanian','Russian','Serbian','Slovak','Slovenian','Spanish','Swahili','Swedish','Thai','Turkish','Ukrainian','Vietnamese','Welsh','Yiddish']
codes=['AF','AX','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ','BS','BH','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BQ','BA','BW','BV','BR','IO','BN','BG','BF','BI','KH','CM','CA','CV','KY','CF','TD','CL','CN','CX','CC','CO','KM','CG','CD','CK','CR','CI','HR','CU','CW','CY','CZ','DK','DJ','DM','DO','EC','EG','SV','GQ','ER','EE','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GG','GN','GW','GY','HT','HM','VA','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IM','IL','IT','JM','JP','JE','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX','FM','MD','MC','MN','ME','MS','MA','MZ','MM','NA','NR','NP','NL','NC','NZ','NI','NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','BL','SH','KN','LC','MF','PM','VC','WS','SM','ST','SA','SN','RS','SC','SL','SG','SX','SK','SI','SB','SO','ZA','GS','ES','LK','SD','SR','SJ','SZ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','US','UM','UY','UZ','VU','VE','VN','VG','VI','WF','EH','YE','ZM','ZW']
match_codes=['AFGHANISTAN','ALAND ISLANDS','ALBANIA','ALGERIA','AMERICAN SAMOA','ANDORRA','ANGOLA','ANGUILLA','ANTARCTICA','ANTIGUA and BARBUDA','ARGENTINA','ARMENIA','ARUBA','AUSTRALIA','AUSTRIA','AZERBAIJAN','BAHAMAS','BAHRAIN','BANGLADESH','BARBADOS','BELARUS','BELGIUM','BELIZE','BENIN','BERMUDA','BHUTAN','BOLIVIA, PLURINATIONAL STATE OF','BONAIRE, SAINT EUSTATIUS and SABA','BOSNIA and HERZEGOVINA','BOTSWANA','BOUVET ISLAND','BRAZIL','BRITISH INDIAN OCEAN TERRITORY','BRUNEI DARUSSALAM','BULGARIA','BURKINA FASO','BURUNDI','CAMBODIA','CAMEROON','CANADA','CAPE VERDE','CAYMAN ISLANDS','CENTRAL AFRICAN REPUBLIC','CHAD','CHILE','CHINA','CHRISTMAS ISLAND','COCOS (KEELING) ISLANDS','COLOMBIA','COMOROS','CONGO','CONGO, THE DEMOCRATIC REPUBLIC OF THE','COOK ISLANDS','COSTA RICA',"COTE D'IVOIRE",'CROATIA','CUBA','CURACAO','CYPRUS','CZECH REPUBLIC','DENMARK','DJIBOUTI','DOMINICA','DOMINICAN REPUBLIC','ECUADOR','EGYPT','EL SALVADOR','EQUATORIAL GUINEA','ERITREA','ESTONIA','ETHIOPIA','FALKLAND ISLANDS (MALVINAS)','FAROE ISLANDS','FIJI','FINLAND','FRANCE','FRENCH GUIANA','FRENCH POLYNESIA','FRENCH SOUTHERN TERRITORIES','GABON','GAMBIA','GEORGIA','GERMANY','GHANA','GIBRALTAR','GREECE','GREENLAND','GRENADA','GUADELOUPE','GUAM','GUATEMALA','GUERNSEY','GUINEA','GUINEA-BISSAU','GUYANA','HAITI','HEARD ISLAND AND MCDONALD ISLANDS','HOLY SEE (VATICAN CITY STATE)','HONDURAS','HONG KONG','HUNGARY','ICELAND','INDIA','INDONESIA','IRAN, ISLAMIC REPUBLIC OF','IRAQ','IRELAND','ISLE OF MAN','ISRAEL','ITALY','JAMAICA','JAPAN','JERSEY','JORDAN','KAZAKHSTAN','KENYA','KIRIBATI',"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",'KOREA, REPUBLIC OF','KUWAIT','KYRGYZSTAN',"LAO PEOPLE'S DEMOCRATIC REPUBLIC",'LATVIA','LEBANON','LESOTHO','LIBERIA','LIBYAN ARAB JAMAHIRIYA','LIECHTENSTEIN','LITHUANIA','LUXEMBOURG','MACAO','MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF','MADAGASCAR','MALAWI','MALAYSIA','MALDIVES','MALI','MALTA','MARSHALL ISLANDS','MARTINIQUE','MAURITANIA','MAURITIUS','MAYOTTE','MEXICO','MICRONESIA, FEDERATED STATES OF','MOLDOVA, REPUBLIC OF','MONACO','MONGOLIA','MONTENEGRO','MONTSERRAT','MOROCCO','MOZAMBIQUE','MYANMAR','NAMIBIA','NAURU','NEPAL','NETHERLANDS','NEW CALEDONIA','NEW ZEALAND','NICARAGUA','NIGER','NIGERIA','NIUE','NORFOLK ISLAND','NORTHERN MARIANA ISLANDS','NORWAY','OMAN','PAKISTAN','PALAU','PALESTINIAN TERRITORY, OCCUPIED','PANAMA','PAPUA NEW GUINEA','PARAGUAY','PERU','PHILIPPINES','PITCAIRN','POLAND','PORTUGAL','PUERTO RICO','QATAR','REUNION','ROMANIA','RUSSIAN FEDERATION','RWANDA','SAINT BARTHELEMY','SAINT HELENA, ASCENSION and TRISTAN DA CUNHA','SAINT KITTS and NEVIS','SAINT LUCIA','SAINT MARTIN (FRENCH PART)','SAINT PIERRE and MIQUELON','SAINT VINCENT and THE GRENADINES','SAMOA','SAN MARINO','SAO TOME and PRINCIPE','SAUDI ARABIA','SENEGAL','SERBIA','SEYCHELLES','SIERRA LEONE','SINGAPORE','SINT MAARTEN (DUTCH PART)','SLOVAKIA','SLOVENIA','SOLOMON ISLANDS','SOMALIA','SOUTH AFRICA','SOUTH GEORGIA and THE SOUTH SANDWICH ISLANDS','SPAIN','SRI LANKA','SUDAN','SURINAME','SVALBARD and JAN MAYEN','SWAZILAND','SWEDEN','SWITZERLAND','SYRIAN ARAB REPUBLIC','TAIWAN, PROVINCE OF CHINA','TAJIKISTAN','TANZANIA, UNITED REPUBLIC OF','THAILAND','TIMOR-LESTE','TOGO','TOKELAU','TONGA','TRINIDAD and TOBAGO','TUNISIA','TURKEY','TURKMENISTAN','TURKS and CAICOS ISLANDS','TUVALU','UGANDA','UKRAINE','UNITED ARAB EMIRATES','UNITED KINGDOM','UNITED STATES','NITED STATES MINOR OUTLYING ISLANDS','URUGUAY','UZBEKISTAN','VANUATU','VENEZUELA, BOLIVARIAN REPUBLIC OF','VIET NAM','VIRGIN ISLANDS, BRITISH','VIRGIN ISLANDS, U.S.','WALLIS and FUTUNA','WESTERN SAHARA','YEMEN','ZAMBIA','ZIMBABWE']
show_possible=['games', 'help', 'version', 'hi', 'randomteam', 'tr', 'lang', 'last', 'online', 'weather', 'lastgame', 'who', 'promote', 'maps', 'say','mapinfo','calc']
### Commands

def games(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        try:
            os.system("wget http://master.open-ra.org/list.php > /dev/null 2>&1")
            filename = "list.php"
            file = open(filename, 'r')
            lines = file.readlines()    #got a list
            file.close()
            os.system("rm list.php")
            length = len(lines)
            if ( length == 1 ):
                if re.search("^#", channel):
                    self.send_message_to_channel( ("No games found"), channel )
                else:
                    self.send_message_to_channel( ("No games found"), user )
            else:
                length = length / 9
                a1=2    #name
                loc=3   #ip
                a2=4    #state
                a3=5    #players
                m=6     #map
                a4=7    #version
                games=''
                count='0'
                for i in range(int(length)):
                    if ( lines[a2].lstrip().rstrip() == 'State: 1' ):
                        count='1'   # lock - there are games in State: 1
                        state = '(W)'
                        ### for location
                        ip=lines[loc].split(':')[1].lstrip()    # ip address
                        os.system("whois "+ip+" > whois_info")
                        filename = 'whois_info'
                        file = open(filename,'r')
                        who = file.readlines()
                        file.close()
                        a =  str(who).split()
                        try:
                            index = a.index('\'country:')
                            index = int(index) + 1
                            code = a[index]
                            code = code[:-4].upper()    #got country code
                            code_index = codes.index(code)
                            country = match_codes[code_index]   #got country name
                        except:
                            country = 'USA' #whois does not show coutry code for most USA IPs and some Canadians (did not find a way to determine where USA and where Canada is)
                        sname = lines[a1].encode('utf-8').decode('utf-8')
                        sname = str(sname)
                        if ( len(sname) == 0 ):
                            sname = 'noname'
                        map_hash = lines[m].split()[1]
                        sql = """SELECT title,players FROM maps
                                WHERE hash = '"""+map_hash+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        for row in cur:
                            pass
                        if ( len(row) != 0 ):
                            map_name = row[0]
                            max_players = '/'+str(row[1])
                        else:
                            map_name = 'unknown'
                            max_players = ''

                        modinfo = lines[a4].strip().split(' ')[1].split('@')

                        games = '@ '+sname.strip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].strip()+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                        if re.search("^#", channel):
                            self.send_message_to_channel( (games), channel )
                        else:
                            self.send_message_to_channel( (games), user )
                    a1=a1+9 
                    loc=loc+9
                    a2=a2+9
                    a3=a3+9
                    m=m+9
                    a4=a4+9
                if ( count == "0" ):    #appeared no games in State: 1
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("No games waiting for players found"), channel )
                    else:
                        self.send_message_to_channel( ("No games waiting for players found"), user )
        except:
            exc = "]games crashed; Request: "+str(command)+"\n"
            filename = 'except_log.txt'
            file = open(filename, 'a')
            file.write(exc)
            file.close()            
    elif ( len(command) == 2 ):   # ]games with args
        try:
            os.system("wget http://master.open-ra.org/list.php > /dev/null 2>&1")
            filename = 'list.php'
            file = open(filename, 'r')
            lines = file.readlines()
            file.close()
            os.system("rm list.php")
            length = len(lines)
            if ( length == 1 ):
                if re.search("^#", channel):
                    self.send_message_to_channel( ("No games found"), channel)
                else:
                    self.send_message_to_channel( ("No games found"), user)
            else:   # there are one or more games
                if ( command[1] == "-w" ):   #request games in State = 1
                    length = length / 9 # number of games
                    a1=2    #name
                    loc=3   #ip
                    a2=4    #state
                    a3=5    #players
                    m=6     #map
                    a4=7    #version
                    count='0'
                    for i in range(int(length)):
                        if ( lines[a2].lstrip().rstrip() == 'State: 1' ):
                            count='1'   # lock - there are games in State: 1
                            state = '(W)'
                            ### for location
                            ip=lines[loc].split(':')[1].lstrip()    # ip address
                            os.system("whois "+ip+" > whois_info")
                            filename = 'whois_info'
                            file = open(filename,'r')
                            who = file.readlines()
                            file.close()
                            a =  str(who).split()
                            try:
                                index = a.index('\'country:')
                                index = int(index) + 1
                                code = a[index]
                                code = code[:-4].upper()    #got country code
                                code_index = codes.index(code)
                                country = match_codes[code_index]
                            except:
                                country = 'USA'
                            sname = lines[a1].encode('utf-8').decode('utf-8')
                            sname = str(sname)
                            if ( len(sname) == 0 ):
                                sname = 'noname'
                            map_hash = lines[m].split()[1]
                            sql = """SELECT title,players FROM maps
                                    WHERE hash = '"""+map_hash+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            for row in cur:
                                pass
                            if ( len(row) != 0 ):
                                map_name = row[0]
                                max_players = '/'+str(row[1])
                            else:
                                map_name = 'unknown'
                                max_players = ''
                            games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                            if re.search("^#", channel):
                                self.send_message_to_channel( (games), channel )
                            else:
                                self.send_message_to_channel( (games), user )
                        a1=a1+9
                        loc=loc+9
                        a2=a2+9
                        a3=a3+9
                        m=m+9
                        a4=a4+9
                    if ( count == "0" ):
                        if re.search("^#", channel):
                            self.send_message_to_channel( ("No games waiting for players found"), channel )
                        else:
                            self.send_message_to_channel( ("No games waiting for players found"), user )           
                elif ( command[1] == "-p" ):     # request games in State = 2
                    length = length / 9 # number of games
                    a1=2    #name
                    loc=3   #ip
                    a2=4    #state
                    a3=5    #players
                    m=6     #map
                    a4=7    #version
                    count = '0'
                    for i in range(int(length)):
                        if ( lines[a2].lstrip().rstrip() == 'State: 2' ):
                            count='1'   # lock - there are games in State: 2
                            state = '(P)'
                            ### for location
                            ip=lines[loc].split(':')[1].lstrip()    # ip address
                            os.system("whois "+ip+" > whois_info")
                            filename = 'whois_info'
                            file = open(filename,'r')
                            who = file.readlines()
                            file.close()
                            a =  str(who).split()
                            try:
                                index = a.index('\'country:')
                                index = int(index) + 1
                                code = a[index]
                                code = code[:-4].upper()    #got country code
                                code_index = codes.index(code)
                                country = match_codes[code_index]
                            except:
                                country = 'USA'
                            sname = lines[a1].encode('utf-8').decode('utf-8')
                            sname = str(sname)
                            if ( len(sname) == 0 ):
                                sname = 'noname'
                            map_hash = lines[m].split()[1]
                            sql = """SELECT title,players FROM maps
                                    WHERE hash = '"""+map_hash+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            for row in cur:
                                pass
                            if ( len(row) != 0 ):
                                map_name = row[0]
                                max_players = '/'+str(row[1])
                            else:
                                map_name = 'unknown'
                                max_players = ''
                            games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                            if re.search("^#", channel):
                                self.send_message_to_channel( (games), channel )
                            else:
                                self.send_message_to_channel( (games), user )
                        a1=a1+9
                        loc=loc+9
                        a2=a2+9
                        a3=a3+9
                        m=m+9
                        a4=a4+9
                    if ( count == "0" ):    #appeared no games in State: 2
                        if re.search("^#", channel):
                            self.send_message_to_channel( ("No started games found"), channel )
                        else:
                            self.send_message_to_channel( ("No started games found"), user )
                elif ( command[1] == "--all" ): # request games in both states
                    length = length / 9 # number of games
                    a1=2    #name
                    loc=3   #ip
                    a2=4    #state
                    a3=5    #players
                    m=6     #map
                    a4=7    #version
                    for i in range(int(length)):
                        if ( lines[a2].lstrip().rstrip() == 'State: 1' ):
                            state = '(W)'
                        elif ( lines[a2].lstrip().rstrip() == 'State: 2' ):
                            state = '(P)'
                        ### for location
                        ip=lines[loc].split(':')[1].lstrip()    # ip address
                        os.system("whois "+ip+" > whois_info")
                        filename = 'whois_info'
                        file = open(filename,'r')
                        who = file.readlines()
                        file.close()
                        a =  str(who).split()
                        try:
                            index = a.index('\'country:')
                            index = int(index) + 1
                            code = a[index]
                            code = code[:-4].upper()    #got country code
                            code_index = codes.index(code)
                            country = match_codes[code_index]
                        except:
                            country = 'USA'
                        sname = lines[a1].encode('utf-8').decode('utf-8')
                        sname = str(sname)
                        if ( len(sname) == 0 ):
                            sname = 'noname'
                        map_hash = lines[m].split()[1]
                        sql = """SELECT title,players FROM maps
                                WHERE hash = '"""+map_hash+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        for row in cur:
                            pass
                        if ( len(row) != 0 ):
                            map_name = row[0]
                            max_players = '/'+str(row[1])
                        else:
                            map_name = 'unknown'
                            max_players = ''
                        games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                        if re.search("^#", channel):
                            self.send_message_to_channel( (games), channel )
                        else:
                            self.send_message_to_channel( (games), user )
                        a1=a1+9
                        loc=loc+9
                        a2=a2+9
                        a3=a3+9
                        m=m+9
                        a4=a4+9
                else:   #it is pattern
                    chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore
                    for i in range(int(len(chars))):
                        if chars[i] in command[1]:
                            check = 'tru'
                            break
                        else:
                            check = 'fals'
                    if ( check == 'fals' ):     #requested pattern does not contain any of 'forbidden' chars
                        p = re.compile(command[1], re.IGNORECASE)
                        length = length / 9 # number of games
                        a1=2    #name
                        loc=3   #ip
                        a2=4    #state
                        a3=5    #players
                        m=6     #map
                        a4=7    #version
                        count='0'
                        for i in range(int(length)):
                            if p.search(lines[a1]):
                                count='1'   # lock
                                if ( lines[a2].lstrip().rstrip() == 'State: 1' ):
                                    state = '(W)'
                                elif ( lines[a2].lstrip().rstrip() == 'State: 2' ):
                                    state = '(P)'
                                ### for location
                                ip=lines[loc].split(':')[1].lstrip()    # ip address
                                os.system("whois "+ip+" > whois_info")
                                filename = 'whois_info'
                                file = open(filename,'r')
                                who = file.readlines()
                                file.close()
                                a =  str(who).split()
                                try:
                                    index = a.index('\'country:')
                                    index = int(index) + 1
                                    code = a[index]
                                    code = code[:-4].upper()    #got country code
                                    code_index = codes.index(code)
                                    country = match_codes[code_index]
                                except:
                                    country = 'USA'
                                sname = lines[a1].encode('utf-8').decode('utf-8')
                                sname = str(sname)
                                if ( len(sname) == 0 ):
                                    sname = 'noname'
                                map_hash = lines[m].split()[1]
                                sql = """SELECT title,players FROM maps
                                        WHERE hash = '"""+map_hash+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                if ( len(row) != 0 ):
                                    map_name = row[0]
                                    max_players = '/'+str(row[1])
                                else:
                                    map_name = 'unknown'
                                    max_players = ''
                                games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                                if re.search("^#", channel):
                                    self.send_message_to_channel( (games), channel)
                                else:
                                    self.send_message_to_channel( (games), user)
                            a1=a1+9
                            loc=loc+9
                            a2=a2+9
                            a3=a3+9
                            m=m+9
                            a4=a4+9
                    if ( count == "0" ):    #appeared no matches
                        if re.search("^#", channel):
                            self.send_message_to_channel( ("No matches"), channel )
                        else:
                            self.send_message_to_channel( ("No matches"), user )
        except:
            exc = "]games crashed; Request: "+str(command)+"\n"
            filename = 'except_log.txt'
            file = open(filename, 'a')
            file.write(exc)
            file.close()
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()

def version(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        url = 'http://openra.res0l.net/download/linux/deb/index.php'
        stream = urllib.request.urlopen(url).read().decode('utf-8')
        release = stream.split('<ul')[1].split('<li>')[1].split('>')[1].split('</a')[0]
        playtest = stream.split('<ul')[2].split('<li>')[1].split('>')[1].split('</a')[0]
        if ( int(release.split('.')[0]) < int(playtest.split('.')[0]) ):
            newer = 'playtest is newer then release'
        else:
            newer = 'release is newer then playtest'
        if re.search("^#", channel):
            self.send_message_to_channel( ("Latest release: "+release[0:4]+""+release[4:8]+" | Latest playtest: "+playtest[0:4]+""+playtest[4:8]+" | "+newer), channel )
        else:
            self.send_message_to_channel( ("Latest release: "+release[0:4]+""+release[4:8]+" | Latest playtest: "+playtest[0:4]+""+playtest[4:8]+" | "+newer), user )
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )

def help(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        if re.search("^#", channel):
            self.send_message_to_channel( ("Help: https://github.com/ihptru/orabot/wiki"), channel )
        else:
            self.send_message_to_channel( ("Help: https://github.com/ihptru/orabot/wiki"), user )
    else:
        if ( command[1] == 'calc' ):
            if ( len(command) == 3 ):
                function = command[2]
                available = vars(math).keys()
                if ( function in available ):
                    desc = eval(function).__doc__.replace('\n',' ')
                    self.send_reply( (desc), user, channel )
                else:
                    self.send_reply( ("I don't know about '"+function+"'"), user, channel )
            else:
                self.send_reply( ("]calc to make calculations"), user, channel )
        else:
            self.send_reply( ("I don't know anything about '"+" ".join(command[1:])+"'"), user, channel )
            
def hi(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        if re.search("^#", channel):
            self.send_message_to_channel( ("Yo " + user + "! Whats up?"), channel )
        else:
            self.send_message_to_channel( ("Yo " + user + "! Whats up?"), user)
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Yo " + user + "! Whats up? And wth is '"+" ".join(command[1:])+"'"), channel )
        else:
            self.send_message_to_channel( ("Yo " + user + "! Whats up? And wth is '"+" ".join(command[1:])+"'"), user )
            
def randomteam(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) > 3 ):
        pyrand.start(self, user, channel, command[1:])
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("You must specify at least 3 teams"), channel)
        else:
            self.send_message_to_channel( ("You must specify at least 3 teams"), user)

def tr(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        message = "Usage: ]tr <from language> <to language> <text to translate>   |   To get a language code, type ]lang <patter>  where <patter> is part of language name  |   For example, to translate from English to German: ]tr en de Thank you"
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
        self.irc_sock.send (str_buff.encode())
    elif ( len(command) > 3 ):
        if command[1] in languages:
            if command[2] in languages:
                filename = 'tr.temp'
                length = len(command)
                line=''
                for i in range(length):
                    line = line+command[i]+' '
                line = line.lstrip().rstrip()
                file = open(filename, 'w')
                file.write(line)
                file.close()
                os.system("python ../tr.py")
                filename = 'tr.text'
                file = open(filename, 'r')
                text = file.readline()
                file.close()
                if re.search("^#", channel):
                    self.send_message_to_channel( (text), channel)
                else:
                    self.send_message_to_channel( (text), user)
            else:
                if re.search("^#", channel):
                    self.send_message_to_channel( ("I don't know such a language: "+command[2]), channel )
                else:
                    self.send_message_to_channel( ("I don't know such a language: "+command[2]), user )
        else:
            if re.search("^#", channel):
                self.send_message_to_channel( ("I don't know such a language: "+command[1]), channel )
            else:
                self.send_message_to_channel( ("I don't know such a language: "+command[1]), user )
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )

def lang(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 2 ):
        re_str = command[1]
        length = int(len(real_langs))
        lang = []
        code = []
        p = re.compile(re_str, re.IGNORECASE)
        for i in range(length):
            if p.search(real_langs[i]):
                lang.append(real_langs[i])
                code.append(languages[i])
        if ( len(lang) > 1 ):
            if re.search("^#", channel):
                self.send_message_to_channel( ("Too many matches, be more specific"), channel)
            else:
                self.send_message_to_channel( ("Too many matches, be more specific"), user)
        elif ( len(lang) == 0 ):
            if re.search("^#", channel):
                self.send_message_to_channel( ("No matches"), channel)
            else:
                self.send_message_to_channel( ("No matches"), user)
        else:
            if re.search("^#", channel):
                self.send_message_to_channel( (code[0] + "      " + lang[0]), channel)
            else:
                self.send_message_to_channel( (code[0] + "      " + lang[0]), user)
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
            
def later(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) >= 3 ):
        if re.search("^#", channel):
            user_nick = command[1] #reciever
            if ( user_nick == user ):
                self.send_message_to_channel( (user+", you can not send a message to yourself"), channel)
            else:
                user_message = " ".join(command[2:])  #message
                #send NAMES channel to server
                str_buff = ( "NAMES %s \r\n" ) % (channel)
                self.irc_sock.send (str_buff.encode())
                #recover all nicks on channel
                recv = self.irc_sock.recv( 4096 )

                if str(recv).find ( "353 orabot =" ) != -1:
                    user_nicks = str(recv).split(':')[2].rstrip()
                    user_nicks = user_nicks.replace('+','').replace('@','')
                    user_nicks = user_nicks.split(' ')
                
                if user_nick in user_nicks:  #reciever is on the channel right now
                    self.send_message_to_channel( (user+", "+user_nick+" is on the channel right now!"), channel)
                else:   #reciever is not on the channel
                    #check if he exists in database
                    sql = """SELECT user FROM users
                            WHERE user = '"""+user_nick+"'"+"""
                    
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = ''
                    for row in cur:
                        pass
                    if user_nick not in row:
                        self.send_message_to_channel( ("Error! No such user in my database"), channel)
                    else:   #users exists
                        #get uid
                        sql = """SELECT * FROM later
                                ORDER BY uid DESC LIMIT 1
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = ''
                        for row in cur:
                            pass
                        uid_later=row[0]
                        uid_later = uid_later + 1
                        sql = """INSERT INTO later
                                (uid,sender,reciever,channel,date,message)
                                VALUES
                                (
                                """+str(uid_later)+",'"+user+"','"+user_nick+"','"+channel+"',strftime('%Y-%m-%d-%H-%M'),'"+user_message.replace("'","~qq~")+"'"+"""
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_message_to_channel( ("The operation succeeded"), channel)
        else:
            self.send_message_to_channel( ("You can use ]later only on a channel"), user)
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Usage: ]later nick message"), channel )
        else:
            self.send_message_to_channel( ("Usage: ]later nick message"), user )
    cur.close()

def last(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        if re.search("^#", channel):
            #send NAMES channel to server
            str_buff = ( "NAMES %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())
            #recover all nicks on channel
            recv = self.irc_sock.recv( 4096 )
            if str(recv).find ( "353 orabot =" ) != -1:
                user_nicks = str(recv).split(':')[2].rstrip()
                user_nicks = user_nicks.replace('+','').replace('@','')
                user_nicks = user_nicks.split(' ')
            
            if command[1] in user_nicks:  #reciever is on the channel right now
                self.send_message_to_channel( ("User is online!"), channel)
                cur.close()
                return
            sql = """SELECT * FROM users
                    WHERE user = '"""+command[1]+"'"+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            if command[1] not in row:   #user not found
                self.send_message_to_channel( ("Error! No such user in my database"), channel)
            else:
                last_time = row[2]
                if ( last_time == None or last_time == '' ):
                    self.send_message_to_channel( ("Sorry, I don't have any record of when user left"), channel)
                else:
                    last_date = "-".join(last_time.split('-')[0:3])
                    last_time = ":".join(last_time.split('-')[3:6])
                    self.send_message_to_channel( (command[1]+" was last seen at "+last_date+" "+last_time+" GMT"), channel)
        else:
            self.send_message_to_channel( ("You can use ]last only on a channel"), user)
    elif ( len(command) == 1 ):
        if re.search("^#", channel):
            self.send_message_to_channel( ("Usage: ]last nick"), channel )
        else:
            self.send_message_to_channel( ("Usage: ]last nick"), user )
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()

def register(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        if not re.search("^#", channel):
            sql = """SELECT * FROM register
                    WHERE user = '"""+user+"'"+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass    
            if user not in row:
                self.send_message_to_channel( ("You are not allowed to register, please contact more privileged user"), user)
            else:   #user found in 'register' database
                ifowner = row[3]
                if ifowner == 0:    #it not 'owner' type of users
                    if row[2] == None:  #password field is empty - this user is set to be registered by owner
                        user_password = command[1]
                        pass_to_db = hashlib.md5( user_password.encode('utf-8') ).hexdigest()
                        sql = """UPDATE register
                                SET pass = '"""+str(pass_to_db)+"'"+"""
                                WHERE user = '"""+user+"'"+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_message_to_channel( ("Congratulations! You are registered. Don't forget your password, you need it to authenticate over ]login password"), user)
                    else:
                        self.send_message_to_channel( ("You are already registered"), user)
        else:
            self.send_message_to_channel( ("Error, ]register can't be used on a channel"), channel )

    elif ( len(command) == 1 ):
        if re.search("^#", channel):
            self.send_message_to_channel( ("Usage: ]register password"), channel )
        else:
            self.send_message_to_channel( ("Usage: ]register password"), user )
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()

def login(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        if not re.search("^#", channel):
            sql = """SELECT * FROM register
                    WHERE user = '"""+user+"'"+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            if ( user not in row ):
                self.send_message_to_channel( ("You are not registered!"), user)
            else:
                if ( row[2] == None ):  #password empty = not registered yet but allowed to
                    self.send_message_to_channel( ("You are not registered!"), user)
                else:   #he is registered
                    if ( row[4] == 1 ):
                        self.send_message_to_channel( ("You are already authenticated!"), user)
                    else:
                        user_password = command[1]
                        user_password_hash = hashlib.md5( user_password.encode('utf-8') ).hexdigest()
                        user_password_hash_in_db = row[2]
                        if ( str(user_password_hash) == str(user_password_hash_in_db) ):    #hashes matches
                            sql = """UPDATE register
                                    SET authenticated = 1
                                    WHERE user = '"""+user+"'"+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_message_to_channel( ("Successful!"), user)
                        else:
                            self.send_message_to_channel( ("Password incorrect!"), user)
        else:
            if re.search("^#", channel):
                self.send_message_to_channel( ("Error, ]login can't be used on a channel"), channel )
            else:
                self.send_message_to_channel( ("Error, ]login can't be used on a channel"), user )
    elif ( len(command) == 1 ):
        if re.search("^#", channel):
            self.send_message_to_channel( ("Usage: ]login password"), channel )
        else:
            self.send_message_to_channel( ("Usage: ]login password"), user )
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()

def online(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        sql = """SELECT * FROM register
                WHERE authenticated = 1
        """
        cur.execute(sql)
        conn.commit()
        row = []
        online = []
        for row in cur:
            online.append(row)
        actual = []
        for i in range(int(len(online))):
            actual.append(online[i][1])
        num_users_online = int(len(actual))
        if ( num_users_online == 0 ):
            if re.search("^#", channel):
                self.send_message_to_channel( ("No any authenticated users online"), channel )
            else:
                self.send_message_to_channel( ("No any authenticated users online"), user )
        else:
            usrs = ", ".join(actual)
            if re.search("^#", channel):
                self.send_message_to_channel( (str(num_users_online)+" authenticated users online: "+usrs), channel )
            else:
                self.send_message_to_channel( (str(num_users_online)+" authenticated users online: "+usrs), user )
    else:
        if re.search("^#", channel):
            self.send_message_to_channel( ("Error, wrong request"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), user )
    cur.close()

def ifuser(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        nick = command[1]
        sql = """SELECT * FROM users
                WHERE user = '"""+nick+"'"+"""
        """
        cur.execute(sql)
        conn.commit()

        row = []
        for row in cur:
            pass
        result = str( nick in row )
        self.send_reply( (result), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()

def adduser(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        sql = """SELECT * FROM register
                WHERE user = '"""+user+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass          # erm, what was the intent here?
        if user in row:
            if row[4] == 0:
                self.send_reply( ("You are not authenticated"), user, channel)
        else:
            self.send_reply( ("You don't have permissions for this command"), user, channel)
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()

def weather(self, user, channel):
    def weather_usage():
        message = "(]weather [--current|--forecast|--all] [US zip code | US/Canada city, state | Foreign city, country]) -- Returns the approximate weather conditions for a given city from Google Weather. --current, --forecast, and --all control what kind of information the command shows."
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
        self.irc_sock.send( str_buff.encode() )

    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        weather_usage()
    elif ( len(command) > 1 ):
        if ( command[1] == "--current" ):
            if ( len(command) == 2 ):
                weather_usage();
            else:
                try:
                    location = command[2]
                    data = pywapi.get_weather_from_google(location)
                    city = data.get("forecast_information").get("city")
                    current = data.get("current_conditions")
                    message = "Current weather for "+city+" | Temperature: "+current.get("temp_c")+"°C; "+current.get("humidity")+"; Conditions: "+current.get("condition")+"; "+current.get("wind_condition")
                    self.send_reply( (message), user, channel )
                except:
                    message = "Error: No such location could be found."
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
        elif (command[1] == "--forecast" ):
            if ( len(command) == 2 ):
                weather_usage()
            else:
                try:
                    location = command[2]
                    data = pywapi.get_weather_from_google(location)
                    city = data.get("forecast_information").get("city")
                    length = len(data.get("forecasts"))
                    weathers = []
                    for i in range(int(length)):
                        day_of_week = data.get("forecasts")[i].get("day_of_week")
                        conditions = data.get("forecasts")[i].get("condition")
                        high_temp = str(int(round((int(data.get("forecasts")[i].get("high"))-32)/1.8)))
                        low_temp = str(int(round((int(data.get("forecasts")[i].get("low"))-32)/1.8)))
                        weathers.append(day_of_week+": "+conditions+"; High of "+high_temp+"°C; Low of "+low_temp+"°C")

                    message = "Forecast for " +city+" | "+" | ".join(weathers)
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                except:
                    message = "Error: No such location could be found."
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
        elif (command[1] == "--all" ):
            if ( len(command) == 2 ):
                weather_usage()
            else:
                try:
                    location = command[2]
                    data = pywapi.get_weather_from_google(location)
                    city = data.get("forecast_information").get("city")
                    current = data.get("current_conditions")
                    length = len(data.get("forecasts"))
                    weathers = []
                    weathers.append("Weather for "+city+" | Temperature: "+current.get("temp_c")+"°C; "+current.get("humidity")+"; Conditions: "+current.get("condition")+"; "+current.get("wind_condition"))
                    for i in range(int(length)):
                        day_of_week = data.get("forecasts")[i].get("day_of_week")
                        conditions = data.get("forecasts")[i].get("condition")
                        high_temp = str(int(round((int(data.get("forecasts")[i].get("high"))-32)/1.8)))
                        low_temp = str(int(round((int(data.get("forecasts")[i].get("low"))-32)/1.8)))
                        weathers.append(day_of_week+": "+conditions+"; High of "+high_temp+"°C; Low of "+low_temp+"°C")
                    message = " | ".join(weathers)
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                except:
                    message = "Error: No such location could be found."
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
        else:
            try:
                location = command[1]
                data = pywapi.get_weather_from_google(location)
                city = data.get("forecast_information").get("city")
                current = data.get("current_conditions")
                message = "Current weather for "+city+" | Temperature: "+current.get("temp_c")+"°C; "+current.get("humidity")+"; Conditions: "+current.get("condition")+"; "+current.get("wind_condition")
                self.send_reply( (message), user, channel )
            except:
                message = "Error: No such location could be found."
                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                self.irc_sock.send (str_buff.encode())

def notify(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if ( user in row ):
            message = "You are already subscribed for new games notification"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
        else:
            sql = """INSERT INTO notify
                    (user,date)
                    VALUES
                    (
                    '"""+user+"',"+"""strftime('%Y-%m-%d-%H-%M-%S')
                    )
            """
            cur.execute(sql)
            conn.commit()
            message = "You are subscribed for new games notification"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
    elif ( len(command) > 1 ):
        length = len(command)
        result_mod = "all"
        result_version = "all"
        result_timeout = "all"
        mod_defined = 0
        version_defined = 0
        timeout_defined = 0
        mods = ['ra','cnc','yf','all']
        timeouts = ['s','m','h','d']
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if ( user in row ):
            message = "You are already subscribed for new games notification"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
            cur.close()
            return
        else:
            for i in range(1,int(length)):
                argument = command[i].split('=')
                if ( len(argument) == 2 ):
                    if ( argument[0] == '-m' ):     #mod
                        if ( mod_defined == 0 ):
                            if ( argument[1].lower() in mods ):
                                mod_defined = 1
                                result_mod = argument[1]
                                sql = """SELECT user FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                if ( user in row ):
                                    sql = """UPDATE notify
                                            SET mod = '"""+argument[1]+"""'
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                else:
                                    sql = """INSERT INTO notify
                                            (user,date,mod)
                                            VALUES
                                            (
                                            '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),'"+argument[1]+"""'
                                            )
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                            else:
                                sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "Error! I don't know such game mod! Try again"
                                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                                self.irc_sock.send (str_buff.encode())
                                cur.close()
                                return 
                        else:
                            sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            message = "Error! You have already defined mod! Try again"
                            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                            self.irc_sock.send (str_buff.encode())
                            cur.close()
                            return
                    elif ( argument[0] == '-v' ):   #version
                        if ( version_defined == 0 ):
                            chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore
                            if ( argument[1] not in chars ):
                                version_defined = 1
                                result_version = "contains "+argument[1]
                                sql = """SELECT user FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                if ( user in row ):
                                    sql = """UPDATE notify
                                            SET version = '"""+argument[1]+"""'
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                else:
                                    sql = """INSERT INTO notify
                                            (user,date,version)
                                            VALUES
                                            (
                                            '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),'"+argument[1]+"""'
                                            )
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                            else:
                                sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "Error! Incorrect version!"
                                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                                self.irc_sock.send (str_buff.encode())
                                cur.close()
                                return
                        else:
                            sql = """DELETE FROM notify
                                    WHERE user = '"""+user+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            message = "Error! You have already defined version! Try again"
                            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                            self.irc_sock.send (str_buff.encode())
                            cur.close()
                            return
                    elif ( argument[0] == '-t' ):   #timeout
                        if ( timeout_defined == 0 ):
                            try:
                                if ( (argument[1] == 'till_quit') or (argument[1] == 'all') or ( argument[1][-1] in timeouts and type(int(argument[1][0:-1])) is int ) ):
                                    timeout_defined = 1
                                    result_timeout = argument[1]
                                    sql = """SELECT user FROM notify
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    row = []
                                    for row in cur:
                                        pass
                                    if ( user in row ):
                                        sql = """UPDATE notify
                                                SET timeout = '"""+argument[1]+"""'
                                                WHERE user = '"""+user+"""'
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                    else:
                                        sql = """INSERT INTO notify
                                                (user,date,timeout)
                                                VALUES
                                                (
                                                '"""+user+"',strftime('%Y-%m-%d-%H-%M-%S'),'"+argument[1]+"""'
                                                )
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                else:
                                    sql = """DELETE FROM notify
                                            WHERE user = '"""+user+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    message = "Timeout Syntax Error! Try again"
                                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                                    self.irc_sock.send (str_buff.encode())
                                    cur.close()
                                    return
                            except:
                                sql = """DELETE FROM notify
                                        WHERE user = '"""+user+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "Timeout Syntax Error! Try again"
                                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                                self.irc_sock.send (str_buff.encode())
                                cur.close()
                                return
                        else:
                            sql = """DELETE FROM notify
                                    WHERE user = '"""+user+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            message = "Error! You have already defined timeout! Try again"
                            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                            self.irc_sock.send (str_buff.encode())
                            cur.close()
                            return
                    else:
                        sql = """DELETE FROM notify
                                WHERE user = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        message = "Syntax error!"+" What is "+argument[0]
                        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                        self.irc_sock.send (str_buff.encode())
                        cur.close()
                        return
                else:
                    sql = """DELETE FROM notify
                            WHERE user = '"""+user+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    message = "Syntax error!"
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                    cur.close()
                    return
            message = "You are subscribed for new games notification; Mod: "+result_mod+"; Version: "+result_version+"; Timeout: "+result_timeout
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
    cur.close()

def unnotify(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        sql = """SELECT user FROM notify
                WHERE user = '"""+user+"""'
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if ( user in row ):
            sql = """DELETE FROM notify
                    WHERE user = '"""+user+"""'
            """
            cur.execute(sql)
            conn.commit()
            message = "You are unsubscribed from new games notification"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
        else:
            message = "You are not subscribed for new games notification"
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
    else:
        message = "Error arguments"
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
        self.irc_sock.send (str_buff.encode())
    cur.close()

def players_for_mode(mode):
    return sum( map( int, mode.split('v') ) )

def add(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if re.search("^#", channel):
        if ( len(command) > 1 ) and ( len(command) < 4 ):   #normal about of arguments
            modes = ['1v1','2v2','3v3','4v4','5v5']
            if ( command[1] not in modes ):
                self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                return
            else:
                host = '0'
                if ( len(command) == 3 ):
                    if ( command[2] == 'host' ):
                        host = '1'  #user can host a game
                    else:
                        self.send_message_to_channel( ("What is '"+command[2]+"'? Try again"), channel )
                        return

                amount_players_required = players_for_mode(command[1])

                #check complaints
                sql = """SELECT name,complaints FROM pickup_stats
                        WHERE name = '"""+user+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if user in row:
                    num_complaints = row[1]
                    if ( int(num_complaints) > 10 ):
                        self.send_message_to_channel( ("You have too many complaints, please contact more privileged user to figure out this issue"), channel )
                        return
                mode = command[1]
                sql = """SELECT name FROM pickup_"""+mode+"""
                        WHERE name = '"""+user+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if user in row:
                    self.send_message_to_channel( ("You are already added for :: "+mode+" :: - Operation failed"), channel )
                    return
                modes.remove(mode)
                diff_mode = ''
                for diff_mode in modes:
                    sql = """SELECT name FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+user+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    if user in row:
                        self.send_message_to_channel( ("You are already added for :: "+diff_mode+" :: - Operation failed"), channel )
                        return
                ### timeout check
                sql = """SELECT name,timeout FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                data = []
                for row in cur:
                    data.append(row)
                if row != []:   #players exist
                    a = date.today()
                    a = str(a)
                    a = a.split('-')
                    year = a[0]
                    month = a[1]
                    day = a[2]
                    b = time.localtime()
                    b = str(b)
                    hours = b.split('tm_hour=')[1].split(',')[0]
                    minutes = b.split('tm_min=')[1].split(',')[0]
                    if len(hours) == 1:
                        hours = '0'+hours
                    else:
                        hours = hours
                    if len(minutes) == 1:
                        minutes = '0'+minutes
                    else:
                        minutes = minutes
                    localtime = year+month+day+hours+minutes
                    data_length = len(data)
                    for i in range(int(data_length)):
                        add_time = "".join(str(data[i][1]).split('-'))
                        remove_user = data[i][0]
                        difference = int(localtime) - int(add_time)
                        if ( difference > 180 ):    #some player was added more then 3 hours ago, remove him
                            sql = """DELETE FROM pickup_"""+mode+"""
                                    WHERE name = '"""+remove_user+"'"+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_message_to_channel( ("@ "+remove_user+" was removed. Reason: Time Out"), channel )
                #generating match
                sql = """SELECT name FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                data = []
                for row in cur:
                    data.append(row)
                data_length = len(data)
                amount_players_left = int(amount_players_required) - int(data_length)
                if ( amount_players_left == 1 ):    # this player is last, check hosts and generate match
                    if ( host == '1' ):
                        sql = """INSERT INTO pickup_"""+mode+"""
                                (name,host,timeout)
                                VALUES
                                ('"""+user+"',"+host+""",strftime('%Y-%m-%d-%H-%M')
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                        self.send_message_to_channel( ("@ "+user+" is successfully added for :: "+mode+" ::"), channel )
                        self.send_message_to_channel( ("@ Enough player detected for :: "+mode+" ::"), channel )
                        sql = """SELECT name FROM pickup_"""+mode+"""
                                WHERE host = 1
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        random_host = []
                        for row in cur:
                            random_host.append(row[0])
                        hoster = random.choice(random_host)
                        sql = """SELECT name FROM pickup_"""+mode+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        name = []
                        for row in cur:
                            name.append(row[0])
                        team1 = []
                        team2 = []
                        while ( len(name) > amount_players_required/2  ):
                            temp_name = random.choice(name)
                            team1.append(temp_name)
                            name.remove(temp_name)
                        team2 = name
                        sql = """SELECT name FROM pickup_maps
                                 WHERE """+"\""+mode+"\""+""" = 1
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        name = []
                        for row in cur:
                            name.append(row[0])
                        map_to_play = random.choice(name)
                        message = "@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(list(team1))+" || Team 2: "+", ".join(list(team2))
                        self.send_message_to_channel( (message), channel )
                        team = team1+team2
                        name = ''
                        for name in team:
                            self.send_message_to_channel( (message), name )
                            if ( hoster == name ):
                                host = 1
                            else:
                                host = 0
                            sql = """SELECT name FROM pickup_stats
                                    WHERE name = '"""+name+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            for row in cur:
                                pass
                            if name not in row:
                                sql = """INSERT INTO pickup_stats
                                        (name,games,hosts,complaints)
                                        VALUES
                                        ('"""+name+"""',1,"""+str(host)+""",0
                                        )
                                """
                                cur.execute(sql)
                                conn.commit()
                            else:
                                sql = """SELECT games,hosts FROM pickup_stats
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                games = row[0]
                                hosts = row[1]
                                games = str(int(games) + 1)
                                hosts = str(int(hosts) + int(host))
                                sql = """UPDATE pickup_stats
                                        SET games = """+games+""", hosts = """+hosts+"""
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                        sql = """DELETE FROM pickup_"""+mode+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                        sql = """INSERT INTO pickup_game_start
                                (team1,team2,type,host,map,time)
                                VALUES
                                ('"""+", ".join(list(team1))+"','"+", ".join(list(team2))+"','"+mode+"','"+hoster+"','"+map_to_play+"',"+"""strftime('%Y-%m-%d-%H-%M')
                                )
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:
                        sql = """SELECT name FROM pickup_"""+mode+"""
                                WHERE host = 1
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        random_host = []
                        for row in cur:
                            random_host.append(row)
                        if ( len(random_host) != 0 ):   #there are hosters
                            sql = """INSERT INTO pickup_"""+mode+"""
                                (name,host,timeout)
                                VALUES
                                ('"""+user+"',"+host+""",strftime('%Y-%m-%d-%H-%M')
                                )
                            """
                            cur.execute(sql)
                            conn.commit()
                            self.send_message_to_channel( ("@ "+user+" is successfully added for :: "+mode+" ::"), channel )
                            self.send_message_to_channel( ("@ Enough player detected for :: "+mode+" ::"), channel )
                            sql = """SELECT name FROM pickup_"""+mode+"""
                                    WHERE host = 1
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            random_host = []
                            for row in cur:
                                random_host.append(row[0])
                            hoster = random.choice(random_host)
                            sql = """SELECT name FROM pickup_"""+mode+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            name = []
                            for row in cur:
                                name.append(row[0])
                            team1 = []
                            team2 = []
                            while ( len(name) > amount_players_required/2  ):
                                temp_name = random.choice(name)
                                team1.append(temp_name)
                                name.remove(temp_name)
                            team2 = name
                            sql = """SELECT name FROM pickup_maps
                                    WHERE """+"\""+mode+"\""+""" = 1
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            name = []
                            for row in cur:
                                name.append(row[0])
                            map_to_play = random.choice(name)
                            message = "@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(list(team1))+" || Team 2: "+", ".join(list(team2))
                            self.send_message_to_channel( (message), channel )
                            team = team1+team2
                            name = ''
                            for name in team:
                                self.send_message_to_channel( (message), name )
                                if ( hoster == name ):
                                    host = 1
                                else:
                                    host = 0
                                sql = """SELECT name FROM pickup_stats
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                for row in cur:
                                    pass
                                if name not in row:
                                    sql = """INSERT INTO pickup_stats
                                            (name,games,hosts,complaints)
                                            VALUES
                                            ('"""+name+"""',1,"""+str(host)+""",0
                                            )
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                else:
                                    sql = """SELECT games,hosts FROM pickup_stats
                                            WHERE name = '"""+name+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    row = []
                                    for row in cur:
                                        pass
                                    games = row[0]
                                    hosts = row[1]
                                    games = str(int(games) + 1)
                                    hosts = str(int(hosts) + int(host))
                                    sql = """UPDATE pickup_stats
                                            SET games = """+games+""", hosts = """+hosts+"""
                                            WHERE name = '"""+name+"""'
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                            sql = """DELETE FROM pickup_"""+mode+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            sql = """INSERT INTO pickup_game_start
                                (team1,team2,type,host,map,time)
                                VALUES
                                ('"""+", ".join(list(team1))+"','"+", ".join(list(team2))+"','"+mode+"','"+hoster+"','"+map_to_play+"',"+"""strftime('%Y-%m-%d-%H-%M')
                                )
                            """
                            cur.execute(sql)
                            conn.commit()
                        else:
                            self.send_message_to_channel( ("@ No any players added, want to be hosters and you are last. You can play only if you can host. Try again"), channel )
                            return

                else:
                    sql = """INSERT INTO pickup_"""+mode+"""
                            (name,host,timeout)
                            VALUES
                            ('"""+user+"',"+host+""",strftime('%Y-%m-%d-%H-%M')
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                    self.send_message_to_channel( ("@ "+user+" is successfully added for :: "+mode+" ::"), channel )
        else:
            self.send_message_to_channel( ("Error, wrong request"), channel )
    else:
        self.send_message_to_channel( ("]add can be used only on a channel"), user )
    cur.close()

def lastgame(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) >= 1 ) and ( len(command) < 3 ):
        if ( len(command) == 1 ):
            sql = """SELECT team1,team2,type,host,map,time FROM pickup_game_start
                    ORDER BY uid DESC LIMIT 1
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            last_date = "-".join(row[5].split('-')[0:3])
            last_time = ":".join(row[5].split('-')[3:5])
            message = "@ "+row[2]+" || Time: "+last_date+" "+last_time+" GMT || Hoster: "+row[3]+" || Map: "+row[4]+" || Team 1: "+row[0]+" || Team 2: "+row[1]
            str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
            self.irc_sock.send (str_buff.encode())
        else:
            modes = ['1v1','2v2','3v3','4v4','5v5']
            if command[1] in modes:
                mode = command[1]
                sql = """SELECT team1,team2,type,host,map,time FROM pickup_game_start
                    WHERE type = '"""+mode+"""'
                    ORDER BY uid DESC LIMIT 1
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if row != []:
                    last_date = "-".join(row[5].split('-')[0:3])
                    last_time = ":".join(row[5].split('-')[3:5])
                    message = "@ "+row[2]+" || Time: "+last_date+" "+last_time+" GMT || Hoster: "+row[3]+" || Map: "+row[4]+" || Team 1: "+row[0]+" || Team 2: "+row[1]
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                else:
                    message = "No "+mode+" games played"
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
            else:
                self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                return
    else:
        self.send_message_to_channel( ("Error, wrong request"), channel )
    cur.close()

def remove(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if re.search("^#", channel):
        if ( len(command) >= 1 ) and ( len(command) < 3 ):
            modes = ['1v1','2v2','3v3','4v4','5v5']
            if ( len(command) == 1 ):
                temp_mode = ''
                for temp_mode in modes:
                    sql = """SELECT name FROM pickup_"""+temp_mode+"""
                            WHERE name = '"""+user+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    if user in row:
                        sql = """DELETE FROM pickup_"""+temp_mode+"""
                                WHERE name = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        message = "You are removed from :: "+temp_mode+" ::"
                        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                        self.irc_sock.send (str_buff.encode())
                        return
                message = "Error, you are not detected added to any game"
                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                self.irc_sock.send (str_buff.encode())
            else:
                if command[1] in modes:
                    mode = command[1]
                    sql = """SELECT name FROM pickup_"""+mode+"""
                            WHERE name = '"""+user+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    if user in row:
                        sql = """DELETE FROM pickup_"""+mode+"""
                                WHERE name = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                        message = "You are removed from :: "+mode+" ::"
                        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                        self.irc_sock.send (str_buff.encode())
                        return
                    message = "Error, you are not detected added to :: "+mode+" ::"
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                else:
                    self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                    return
        else:
            self.send_message_to_channel( ("Error, wrong request"), channel )
    else:
        self.send_message_to_channel( ("]remove can be used only on a channel"), user )
    cur.close()

def who(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) >= 1 ) and ( len(command) < 3 ):
        modes = ['1v1','2v2','3v3','4v4','5v5']
        if ( len(command) == 1 ):
            temp_mode = ''
            names = []
            for temp_mode in modes:
                amount_players_required = players_for_mode( temp_mode )
                sql = """SELECT name,host FROM pickup_"""+temp_mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                name = []
                for row in cur:
                    if ( row[1] == 1 ):
                        name.append(row[0]+"[h]")
                    else:
                        name.append(row[0])
                if name != []:
                    names.append(temp_mode + " ["+str(len(name))+"/"+str(amount_players_required)+"]: " + ", ".join(name))
            if names == []:
                message = "No game going on!"
                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                self.irc_sock.send (str_buff.encode())
            else:
                message = "All games: "+" || ".join(names)
                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                self.irc_sock.send (str_buff.encode())
        else:
            if command[1] in modes:
                mode = command[1]
                amount_players_required = players_for_mode( mode )
                sql = """SELECT name,host FROM pickup_"""+mode+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                name = []
                for row in cur:
                    if ( row[1] == 1 ):
                        name.append(row[0]+"[h]")
                    else:
                        name.append(row[0])
                if name == []:
                    message = "No players detected for :: "+mode+" ::"
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                else:
                    message = "@ " + mode + " ["+str(len(name))+"/"+str(amount_players_required)+"]: " + ", ".join(name)
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
            else:
                self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                return

    else:
        self.send_message_to_channel( ("Error, wrong request"), channel )
    cur.close()

def promote(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 2 ):
        modes = ['1v1','2v2','3v3','4v4','5v5']
        mode = command[1]
        if mode in modes:
            amount_players_required = players_for_mode( mode )
            sql = """SELECT name FROM pickup_"""+mode+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            name = []
            for row in cur:
                name.append(row[0])
            if ( name == [] ):
                message = "Promote Error, no players added for "+mode
                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                self.irc_sock.send (str_buff.encode())
            else:
                message = "Please add up for :: "+mode+" :: ! "+ str(amount_players_required-int(len(name))) + " more people needed! (Type ]add "+mode+"  or  ]add "+mode+" host  ,if you can host)"
                self.send_message_to_channel( (message), channel )
        else:
            self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
            return
    elif ( len(command) > 2 ):
        self.send_message_to_channel( ("Error, wrong request"), channel )
    else:
        message = "Specify mode type to promote! 1v1, 2v2, 3v3, 4v4 or 5v5"
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
        self.irc_sock.send (str_buff.encode())
    cur.close()

def maps(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        self.send_reply( ("Pickup Matches Maps: https://github.com/ihptru/orabot/wiki/Pickup-Maps"), user, channel )
    else:
        self.send_reply( ("I don't know anything about '"+" ".join(command[1:])+"'"), user, channel )

def say(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) > 1 ):
        self.send_reply( (" ".join(command[1:])), user, channel )

def show(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) >= 4 ):
        if ( command[-2] == '|' ):
            to_user = command[-1]

            if re.search("^#", channel):
                #send NAMES channel to server
                str_buff = ( "NAMES %s \r\n" ) % (channel)
                self.irc_sock.send (str_buff.encode())
                #recover all nicks on channel
                recv = self.irc_sock.recv( 4096 )

                if str(recv).find ( "353 orabot =" ) != -1:
                    user_nicks = str(recv).split(':')[2].rstrip()
                    user_nicks = user_nicks.replace('+','').replace('@','')
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
                eval (show_command[0])(self, to_user, to_user)
            else:
                self.send_reply( ("I can not show output of this command to user"), user, channel )
        else:
            self.send_reply( ("Syntax error"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    
def mapinfo(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 1 ):
        self.send_reply( ("Part of map's name required!"), user, channel )
    else:
        if ( command[1] == '--random' ):
            if ( len(command) == 2 ):
                sql = """SELECT mod,title,description,author,type,titleset,players FROM maps
                        ORDER BY RANDOM() LIMIT 1
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if ( row[2] == '' ):
                    description = ''
                else:
                    description = " - Description: "+row[2]
                self.send_reply( ("Map name: "+row[1]+" - Mod: "+row[0]+description+" - Author: "+row[3]+" - Max Players: "+str(row[6])+" - Type: "+row[4]+" - Titleset: "+row[5]), user, channel )
            else:
                self.send_reply( ("Error, wrong request"), user, channel )
        else:
            mods = ['ra','cnc','yf']
            cond = command[1].split('=')
            if ( cond[0] == '--mod' ):
                if ( cond[1] != '' ):
                    mod = cond[1]
                    if ( mod not in mods ):
                        self.send_reply( ("I don't know such a mod!"), user, channel )
                        cur.close()
                        return
                    else:
                        map_pattern = " ".join(command[2:])
            else:
                map_pattern = " ".join(command[1:])
                mod = ''
            sql = """SELECT mod,title,description,author,type,titleset,players FROM maps
                    WHERE upper(title) LIKE upper('%"""+map_pattern+"""%') and upper(mod) LIKE upper('%"""+mod+"""%')
            """
            cur.execute(sql)
            conn.commit()
            row = []
            data = []
            for row in cur:
                data.append(row)
            if ( len(data) == 0 ):
                self.send_reply( ("Map is not found!"), user, channel )
                cur.close()
                return
            elif ( len(data) == 1 ):
                if ( row[2] == '' ):
                    description = ''
                else:
                    description = " - Description: "+row[2]
                self.send_reply( ("Map name: "+row[1]+" - Mod: "+row[0]+description+" - Author: "+row[3]+" - Max Players: "+str(row[6])+" - Type: "+row[4]+" - Titleset: "+row[5]), user, channel )
            else:
                self.send_reply( ("Too many matches!"), user, channel )
                cur.close()
                return
    cur.close()

def calc(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) > 1 ):
        expr = " ".join(command[1:])
        expr = expr.replace('^','**')
        def safe_eval(expr, symbols={}):
            return eval(expr, dict(__builtins__=None), symbols)
        
        def calc(expr):
            return safe_eval(expr, vars(math))
    
        try:
            result = calc(expr)
            self.send_reply( (result), user, channel )
        except:
            self.send_reply( ("Error encountered!"), user, channel )
    else:
        functions = 'pow, fsum, cosh, ldexp, hypot, acosh, tan, asin, isnan, log, fabs, floor, atanh, modf, sqrt, frexp, degrees, pi, log10, asinh, exp, atan, factorial, copysign, ceil, isinf, sinh, trunc, cos, e, tanh, radians, sin, atan2, fmod, acos, log1p'
        self.send_reply( ("Available functions: "+functions), user, channel )
