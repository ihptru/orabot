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

import sys
import traceback
import pygeoip
import sqlite3
import re
import urllib.request
import time

codes=['AF','AX','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ','BS','BH','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BQ','BA','BW','BV','BR','IO','BN','BG','BF','BI','KH','CM','CA','CV','KY','CF','TD','CL','CN','CX','CC','CO','KM','CG','CD','CK','CR','CI','HR','CU','CW','CY','CZ','DK','DJ','DM','DO','EC','EG','SV','GQ','ER','EE','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GG','GN','GW','GY','HT','HM','VA','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IM','IL','IT','JM','JP','JE','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX','FM','MD','MC','MN','ME','MS','MA','MZ','MM','NA','NR','NP','NL','NC','NZ','NI','NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','BL','SH','KN','LC','MF','PM','VC','WS','SM','ST','SA','SN','RS','SC','SL','SG','SX','SK','SI','SB','SO','ZA','GS','ES','LK','SD','SR','SJ','SZ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','US','UM','UY','UZ','VU','VE','VN','VG','VI','WF','EH','YE','ZM','ZW']
match_codes=['AFGHANISTAN','ALAND ISLANDS','ALBANIA','ALGERIA','AMERICAN SAMOA','ANDORRA','ANGOLA','ANGUILLA','ANTARCTICA','ANTIGUA and BARBUDA','ARGENTINA','ARMENIA','ARUBA','AUSTRALIA','AUSTRIA','AZERBAIJAN','BAHAMAS','BAHRAIN','BANGLADESH','BARBADOS','BELARUS','BELGIUM','BELIZE','BENIN','BERMUDA','BHUTAN','BOLIVIA, PLURINATIONAL STATE OF','BONAIRE, SAINT EUSTATIUS and SABA','BOSNIA and HERZEGOVINA','BOTSWANA','BOUVET ISLAND','BRAZIL','BRITISH INDIAN OCEAN TERRITORY','BRUNEI DARUSSALAM','BULGARIA','BURKINA FASO','BURUNDI','CAMBODIA','CAMEROON','CANADA','CAPE VERDE','CAYMAN ISLANDS','CENTRAL AFRICAN REPUBLIC','CHAD','CHILE','CHINA','CHRISTMAS ISLAND','COCOS (KEELING) ISLANDS','COLOMBIA','COMOROS','CONGO','CONGO, THE DEMOCRATIC REPUBLIC OF THE','COOK ISLANDS','COSTA RICA',"COTE D'IVOIRE",'CROATIA','CUBA','CURACAO','CYPRUS','CZECH REPUBLIC','DENMARK','DJIBOUTI','DOMINICA','DOMINICAN REPUBLIC','ECUADOR','EGYPT','EL SALVADOR','EQUATORIAL GUINEA','ERITREA','ESTONIA','ETHIOPIA','FALKLAND ISLANDS (MALVINAS)','FAROE ISLANDS','FIJI','FINLAND','FRANCE','FRENCH GUIANA','FRENCH POLYNESIA','FRENCH SOUTHERN TERRITORIES','GABON','GAMBIA','GEORGIA','GERMANY','GHANA','GIBRALTAR','GREECE','GREENLAND','GRENADA','GUADELOUPE','GUAM','GUATEMALA','GUERNSEY','GUINEA','GUINEA-BISSAU','GUYANA','HAITI','HEARD ISLAND AND MCDONALD ISLANDS','HOLY SEE (VATICAN CITY STATE)','HONDURAS','HONG KONG','HUNGARY','ICELAND','INDIA','INDONESIA','IRAN, ISLAMIC REPUBLIC OF','IRAQ','IRELAND','ISLE OF MAN','ISRAEL','ITALY','JAMAICA','JAPAN','JERSEY','JORDAN','KAZAKHSTAN','KENYA','KIRIBATI',"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",'KOREA, REPUBLIC OF','KUWAIT','KYRGYZSTAN',"LAO PEOPLE'S DEMOCRATIC REPUBLIC",'LATVIA','LEBANON','LESOTHO','LIBERIA','LIBYAN ARAB JAMAHIRIYA','LIECHTENSTEIN','LITHUANIA','LUXEMBOURG','MACAO','MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF','MADAGASCAR','MALAWI','MALAYSIA','MALDIVES','MALI','MALTA','MARSHALL ISLANDS','MARTINIQUE','MAURITANIA','MAURITIUS','MAYOTTE','MEXICO','MICRONESIA, FEDERATED STATES OF','MOLDOVA, REPUBLIC OF','MONACO','MONGOLIA','MONTENEGRO','MONTSERRAT','MOROCCO','MOZAMBIQUE','MYANMAR','NAMIBIA','NAURU','NEPAL','NETHERLANDS','NEW CALEDONIA','NEW ZEALAND','NICARAGUA','NIGER','NIGERIA','NIUE','NORFOLK ISLAND','NORTHERN MARIANA ISLANDS','NORWAY','OMAN','PAKISTAN','PALAU','PALESTINIAN TERRITORY, OCCUPIED','PANAMA','PAPUA NEW GUINEA','PARAGUAY','PERU','PHILIPPINES','PITCAIRN','POLAND','PORTUGAL','PUERTO RICO','QATAR','REUNION','ROMANIA','RUSSIAN FEDERATION','RWANDA','SAINT BARTHELEMY','SAINT HELENA, ASCENSION and TRISTAN DA CUNHA','SAINT KITTS and NEVIS','SAINT LUCIA','SAINT MARTIN (FRENCH PART)','SAINT PIERRE and MIQUELON','SAINT VINCENT and THE GRENADINES','SAMOA','SAN MARINO','SAO TOME and PRINCIPE','SAUDI ARABIA','SENEGAL','SERBIA','SEYCHELLES','SIERRA LEONE','SINGAPORE','SINT MAARTEN (DUTCH PART)','SLOVAKIA','SLOVENIA','SOLOMON ISLANDS','SOMALIA','SOUTH AFRICA','SOUTH GEORGIA and THE SOUTH SANDWICH ISLANDS','SPAIN','SRI LANKA','SUDAN','SURINAME','SVALBARD and JAN MAYEN','SWAZILAND','SWEDEN','SWITZERLAND','SYRIAN ARAB REPUBLIC','TAIWAN, PROVINCE OF CHINA','TAJIKISTAN','TANZANIA, UNITED REPUBLIC OF','THAILAND','TIMOR-LESTE','TOGO','TOKELAU','TONGA','TRINIDAD and TOBAGO','TUNISIA','TURKEY','TURKMENISTAN','TURKS and CAICOS ISLANDS','TUVALU','UGANDA','UKRAINE','UNITED ARAB EMIRATES','UNITED KINGDOM','UNITED STATES','NITED STATES MINOR OUTLYING ISLANDS','URUGUAY','UZBEKISTAN','VANUATU','VENEZUELA, BOLIVARIAN REPUBLIC OF','VIET NAM','VIRGIN ISLANDS, BRITISH','VIRGIN ISLANDS, U.S.','WALLIS and FUTUNA','WESTERN SAHARA','YEMEN','ZAMBIA','ZIMBABWE']

def games(self, user, channel):
    command = (self.command)
    command = command.split()
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    flood_protection = 0
    if ( len(command) == 1 ):
        try:
            url = 'http://master.open-ra.org/list.php'
            stream = urllib.request.urlopen(url).read()
            stream = stream.decode('utf-8')
            lines = []
            sep_games = stream.split('\nGame')
            for i in range(int(len(sep_games))):
                lines =  lines + sep_games[i].split('\n\t') #got a list
            length = len(lines)
            if ( length == 1 ):
                self.send_reply( ("No games found"), user, channel )
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
                        gi = pygeoip.GeoIP('../GeoIP.dat')
                        code = gi.country_code_by_addr(ip)  #got country code
                        code_index = codes.index(code)
                        country = match_codes[code_index]   #got country name
                        
                        sname = str(lines[a1].encode('utf-8').decode('utf-8'))
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
                        modinfo = " ".join(lines[a4].strip().split(' ')[1:]).split('@')
                        games = '@ '+sname.strip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].strip()+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                        time.sleep(0.5)
                        flood_protection = flood_protection + 1
                        if flood_protection == 7:
                            time.sleep(5)
                            flood_protection = 0
                        self.send_reply( (games), user, channel )
                    a1=a1+9 
                    loc=loc+9
                    a2=a2+9
                    a3=a3+9
                    m=m+9
                    a4=a4+9
                flood_protection = 0
                if ( count == "0" ):    #appeared no games in State: 1
                    self.send_reply( ("No games waiting for players found"), user, channel )
        except:
            exc = "Crash; Request: "+str(command)+" | "+str(sys.exc_info())+"\n"+str(traceback.format_exc())+"\n"
            filename = 'except.log'
            file = open(filename, 'a')
            file.write(exc)
            file.close()            
    elif ( len(command) == 2 ):   # ]games with args
        try:
            url = 'http://master.open-ra.org/list.php'
            stream = urllib.request.urlopen(url).read()
            stream = stream.decode('utf-8')
            lines = []
            sep_games = stream.split('\nGame')
            for i in range(int(len(sep_games))):
                lines =  lines + sep_games[i].split('\n\t') #got a list
            length = len(lines)
            if ( length == 1 ):
                self.send_reply( ("No games found"), user, channel )
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
                            gi = pygeoip.GeoIP('../GeoIP.dat')
                            code = gi.country_code_by_addr(ip)  #got country code
                            code_index = codes.index(code)
                            country = match_codes[code_index]
                            
                            sname = str(lines[a1].encode('utf-8').decode('utf-8'))
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
                            modinfo = " ".join(lines[a4].strip().split(' ')[1:]).split('@')
                            games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                            time.sleep(0.5)
                            flood_protection = flood_protection + 1
                            if flood_protection == 7:
                                time.sleep(5)
                                flood_protection = 0
                            self.send_reply( (games), user, channel )
                        a1=a1+9
                        loc=loc+9
                        a2=a2+9
                        a3=a3+9
                        m=m+9
                        a4=a4+9
                    flood_protection = 0
                    if ( count == "0" ):
                        self.send_reply( ("No games waiting for players found"), user, channel )
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
                            gi = pygeoip.GeoIP('../GeoIP.dat')
                            code = gi.country_code_by_addr(ip)  #got country code
                            code_index = codes.index(code)
                            country = match_codes[code_index]
                            
                            sname = str(lines[a1].encode('utf-8').decode('utf-8'))
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
                            modinfo = " ".join(lines[a4].strip().split(' ')[1:]).split('@')
                            games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                            time.sleep(0.5)
                            flood_protection = flood_protection + 1
                            if flood_protection == 7:
                                time.sleep(5)
                                flood_protection = 0
                            self.send_reply( (games), user, channel )
                        a1=a1+9
                        loc=loc+9
                        a2=a2+9
                        a3=a3+9
                        m=m+9
                        a4=a4+9
                    flood_protection = 0
                    if ( count == "0" ):    #appeared no games in State: 2
                        self.send_reply( ("No started games found"), user, channel )
                elif ( (command[1] == "--all") or (command[1] == "-wp") ): # request games in both states
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
                        gi = pygeoip.GeoIP('../GeoIP.dat')
                        code = gi.country_code_by_addr(ip)  #got country code
                        code_index = codes.index(code)
                        country = match_codes[code_index]
                        
                        sname = str(lines[a1].encode('utf-8').decode('utf-8'))
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
                        modinfo = " ".join(lines[a4].strip().split(' ')[1:]).split('@')
                        games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                        time.sleep(0.5)
                        flood_protection = flood_protection + 1
                        if flood_protection == 7:
                            time.sleep(5)
                            flood_protection = 0
                        self.send_reply( (games), user, channel )
                        a1=a1+9
                        loc=loc+9
                        a2=a2+9
                        a3=a3+9
                        m=m+9
                        a4=a4+9
                    flood_protection = 0
                elif ( (command[1]) == "-s" ):
                    length = length / 9 # number of games
                    a1=2    #name
                    a2=4    #state
                    a3=5    #players
                    a4=7    #version
                    games_state1 = ''
                    games_state2 = ''
                    for i in range(int(length)):
                        if ( lines[a2].lstrip().rstrip() == 'State: 1' ):
                            state = 'W'
                        elif ( lines[a2].lstrip().rstrip() == 'State: 2' ):
                            state = 'P'
                        
                        sname = str(lines[a1].encode('utf-8').decode('utf-8'))
                        if ( len(sname) == 0 ):
                            sname = 'noname'
                        modinfo = " ".join(lines[a4].strip().split(' ')[1:]).split('@')
                        if ( state == 'W' ):
                            games_state1 = games_state1+'\t['+lines[a3].lstrip().rstrip().split()[1]+'] '+sname.lstrip().rstrip()[6:].lstrip()+' ('+(modinfo[0].upper()+'@'+ modinfo[1])+')||'
                        elif ( state == 'P' ):
                            games_state2 = games_state2+'\t['+lines[a3].lstrip().rstrip().split()[1]+'] '+sname.lstrip().rstrip()[6:].lstrip()+' ('+(modinfo[0].upper()+'@'+ modinfo[1])+')||'
                        a1=a1+9
                        a2=a2+9
                        a3=a3+9
                        a4=a4+9
                    split_games_state1 = games_state1.split('||')
                    split_games_state2 = games_state2.split('||')
                    if ( len(split_games_state2) > 1 ):
                        self.send_reply( ('Playing:'), user, channel )
                        for i in range(int(len(split_games_state2) - 1)):
                            flood_protection = flood_protection + 1
                            if flood_protection == 7:
                                time.sleep(5)
                                flood_protection = 0
                            self.send_reply( (split_games_state2[i]), user, channel )
                            time.sleep(0.5)
                    if ( len(split_games_state1) > 1 ):
                        self.send_reply( ('Waiting:'), user, channel )
                        for i in range(int(len(split_games_state1) - 1)):
                            flood_protection = flood_protection + 1
                            if flood_protection == 7:
                                time.sleep(5)
                                flood_protection = 0
                            self.send_reply( (split_games_state1[i]), user, channel )
                            time.sleep(0.5)
                    flood_protection = 0
                elif ( (command[1]) == "-r" ):
                    self.send_reply( ("A pattern required"), user, channel )
                else:
                    self.send_reply( ("Incorrect option!"), user, channel )                    
        except:
            exc = "Crash; Request: "+str(command)+" | "+str(sys.exc_info())+"\n"+str(traceback.format_exc())+"\n"
            filename = 'except_log.txt'
            file = open(filename, 'a')
            file.write(exc)
            file.close()
    elif ( len(command) > 2 ):
        if ( command[1] == "-r" ):  #patter request
            try:
                url = 'http://master.open-ra.org/list.php'
                stream = urllib.request.urlopen(url).read()
                stream = stream.decode('utf-8')
                lines = []
                sep_games = stream.split('\nGame')
                for i in range(int(len(sep_games))):
                    lines =  lines + sep_games[i].split('\n\t') #got a list
                length = len(lines)
                if ( length == 1 ):
                    self.send_reply( ("No games found"), user, channel )
                else:   # there are one or more games
                    chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore
                    request_pattern = " ".join(command[2:])
                    for i in range(int(len(chars))):
                        if chars[i] in request_pattern:
                            check = 'tru'
                            break
                        else:
                            check = 'fals'
                    if ( check == 'fals' ):     #requested pattern does not contain any of 'forbidden' chars
                        p = re.compile(request_pattern, re.IGNORECASE)
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
                                gi = pygeoip.GeoIP('../GeoIP.dat')
                                code = gi.country_code_by_addr(ip)  #got country code
                                code_index = codes.index(code)
                                country = match_codes[code_index]

                                sname = str(lines[a1].encode('utf-8').decode('utf-8'))
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
                                modinfo = " ".join(lines[a4].strip().split(' ')[1:]).split('@')
                                games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(15)+' - '+state+' - '+lines[a3].lstrip().rstrip()+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                                time.sleep(0.5)
                                flood_protection = flood_protection + 1
                                if flood_protection == 7:
                                    time.sleep(5)
                                    flood_protection = 0
                                self.send_reply( (games), user, channel )
                            a1=a1+9
                            loc=loc+9
                            a2=a2+9
                            a3=a3+9
                            m=m+9
                            a4=a4+9
                        flood_protection = 0
                        if ( count == "0" ):    #appeared no matches
                            self.send_reply( ("No matches"), user, channel )
            except:
                exc = "Crash; Request: "+str(command)+" | "+str(sys.exc_info())+"\n"+str(traceback.format_exc())+"\n"
                filename = 'except_log.txt'
                file = open(filename, 'a')
                file.write(exc)
                file.close()
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()
