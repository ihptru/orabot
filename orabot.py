#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This code was written for Python 3.1.1
# version 0.101

# Changelog:
# version 0.100
# Basic framework
#
# version 0.101
# Fixed an error if an admin used a command with an argument, that wasn't an admin-only command

import socket, sys, threading, time
import os
import re
from datetime import date
# Hardcoding the root admin - it seems the best way for now
root_admin = "ihptru"

languages=['af','sq','ar','be','bg','ca','zh-CN','hr','cs','da','nl','en','et','tl','fi','fr','gl','de','el','iw','hi','hu','is','id','ga','it','ja','ko','lv','lt','mk','ml','mt','no','fa','pl','ro','ru','sr','sk','sl','es','sw','sv','th','tr','uk','vi','cy','yi']
real_langs=['Afrikaans','Albanian','Arabic','Belarusian','Bulgarian','Catalan','Chinese_Simplified','Croatian','Czech','Danish','Dutch','English','Estonian','Filipino','Finnish','French','Galician','German','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Irish','Italian','Japanese','Korean','Latvian','Lithuanian','Macedonian','Malay','Maltese','Norwegian','Persian','Polish','Romanian','Russian','Serbian','Slovak','Slovenian','Spanish','Swahili','Swedish','Thai','Turkish','Ukrainian','Vietnamese','Welsh','Yiddish']
codes=['AF','AX','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ','BS','BH','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BQ','BA','BW','BV','BR','IO','BN','BG','BF','BI','KH','CM','CA','CV','KY','CF','TD','CL','CN','CX','CC','CO','KM','CG','CD','CK','CR','CI','HR','CU','CW','CY','CZ','DK','DJ','DM','DO','EC','EG','SV','GQ','ER','EE','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GG','GN','GW','GY','HT','HM','VA','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IM','IL','IT','JM','JP','JE','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX','FM','MD','MC','MN','ME','MS','MA','MZ','MM','NA','NR','NP','NL','NC','NZ','NI','NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','BL','SH','KN','LC','MF','PM','VC','WS','SM','ST','SA','SN','RS','SC','SL','SG','SX','SK','SI','SB','SO','ZA','GS','ES','LK','SD','SR','SJ','SZ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','US','UM','UY','UZ','VU','VE','VN','VG','VI','WF','EH','YE','ZM','ZW']
match_codes=['AFGHANISTAN','ALAND ISLANDS','ALBANIA','ALGERIA','AMERICAN SAMOA','ANDORRA','ANGOLA','ANGUILLA','ANTARCTICA','ANTIGUA and BARBUDA','ARGENTINA','ARMENIA','ARUBA','AUSTRALIA','AUSTRIA','AZERBAIJAN','BAHAMAS','BAHRAIN','BANGLADESH','BARBADOS','BELARUS','BELGIUM','BELIZE','BENIN','BERMUDA','BHUTAN','BOLIVIA, PLURINATIONAL STATE OF','BONAIRE, SAINT EUSTATIUS and SABA','BOSNIA and HERZEGOVINA','BOTSWANA','BOUVET ISLAND','BRAZIL','BRITISH INDIAN OCEAN TERRITORY','BRUNEI DARUSSALAM','BULGARIA','BURKINA FASO','BURUNDI','CAMBODIA','CAMEROON','CANADA','CAPE VERDE','CAYMAN ISLANDS','CENTRAL AFRICAN REPUBLIC','CHAD','CHILE','CHINA','CHRISTMAS ISLAND','COCOS (KEELING) ISLANDS','COLOMBIA','COMOROS','CONGO','CONGO, THE DEMOCRATIC REPUBLIC OF THE','COOK ISLANDS','COSTA RICA',"COTE D'IVOIRE",'CROATIA','CUBA','CURACAO','CYPRUS','CZECH REPUBLIC','DENMARK','DJIBOUTI','DOMINICA','DOMINICAN REPUBLIC','ECUADOR','EGYPT','EL SALVADOR','EQUATORIAL GUINEA','ERITREA','ESTONIA','ETHIOPIA','FALKLAND ISLANDS (MALVINAS)','FAROE ISLANDS','FIJI','FINLAND','FRANCE','FRENCH GUIANA','FRENCH POLYNESIA','FRENCH SOUTHERN TERRITORIES','GABON','GAMBIA','GEORGIA','GERMANY','GHANA','GIBRALTAR','GREECE','GREENLAND','GRENADA','GUADELOUPE','GUAM','GUATEMALA','GUERNSEY','GUINEA','GUINEA-BISSAU','GUYANA','HAITI','HEARD ISLAND AND MCDONALD ISLANDS','HOLY SEE (VATICAN CITY STATE)','HONDURAS','HONG KONG','HUNGARY','ICELAND','INDIA','INDONESIA','IRAN, ISLAMIC REPUBLIC OF','IRAQ','IRELAND','ISLE OF MAN','ISRAEL','ITALY','JAMAICA','JAPAN','JERSEY','JORDAN','KAZAKHSTAN','KENYA','KIRIBATI',"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",'KOREA, REPUBLIC OF','KUWAIT','KYRGYZSTAN',"LAO PEOPLE'S DEMOCRATIC REPUBLIC",'LATVIA','LEBANON','LESOTHO','LIBERIA','LIBYAN ARAB JAMAHIRIYA','LIECHTENSTEIN','LITHUANIA','LUXEMBOURG','MACAO','MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF','MADAGASCAR','MALAWI','MALAYSIA','MALDIVES','MALI','MALTA','MARSHALL ISLANDS','MARTINIQUE','MAURITANIA','MAURITIUS','MAYOTTE','MEXICO','MICRONESIA, FEDERATED STATES OF','MOLDOVA, REPUBLIC OF','MONACO','MONGOLIA','MONTENEGRO','MONTSERRAT','MOROCCO','MOZAMBIQUE','MYANMAR','NAMIBIA','NAURU','NEPAL','NETHERLANDS','NEW CALEDONIA','NEW ZEALAND','NICARAGUA','NIGER','NIGERIA','NIUE','NORFOLK ISLAND','NORTHERN MARIANA ISLANDS','NORWAY','OMAN','PAKISTAN','PALAU','PALESTINIAN TERRITORY, OCCUPIED','PANAMA','PAPUA NEW GUINEA','PARAGUAY','PERU','PHILIPPINES','PITCAIRN','POLAND','PORTUGAL','PUERTO RICO','QATAR','REUNION','ROMANIA','RUSSIAN FEDERATION','RWANDA','SAINT BARTHELEMY','SAINT HELENA, ASCENSION and TRISTAN DA CUNHA','SAINT KITTS and NEVIS','SAINT LUCIA','SAINT MARTIN (FRENCH PART)','SAINT PIERRE and MIQUELON','SAINT VINCENT and THE GRENADINES','SAMOA','SAN MARINO','SAO TOME and PRINCIPE','SAUDI ARABIA','SENEGAL','SERBIA','SEYCHELLES','SIERRA LEONE','SINGAPORE','SINT MAARTEN (DUTCH PART)','SLOVAKIA','SLOVENIA','SOLOMON ISLANDS','SOMALIA','SOUTH AFRICA','SOUTH GEORGIA and THE SOUTH SANDWICH ISLANDS','SPAIN','SRI LANKA','SUDAN','SURINAME','SVALBARD and JAN MAYEN','SWAZILAND','SWEDEN','SWITZERLAND','SYRIAN ARAB REPUBLIC','TAIWAN, PROVINCE OF CHINA','TAJIKISTAN','TANZANIA, UNITED REPUBLIC OF','THAILAND','TIMOR-LESTE','TOGO','TOKELAU','TONGA','TRINIDAD and TOBAGO','TUNISIA','TURKEY','TURKMENISTAN','TURKS and CAICOS ISLANDS','TUVALU','UGANDA','UKRAINE','UNITED ARAB EMIRATES','UNITED KINGDOM','UNITED STATES','NITED STATES MINOR OUTLYING ISLANDS','URUGUAY','UZBEKISTAN','VANUATU','VENEZUELA, BOLIVARIAN REPUBLIC OF','VIET NAM','VIRGIN ISLANDS, BRITISH','VIRGIN ISLANDS, U.S.','WALLIS and FUTUNA','WESTERN SAHARA','YEMEN','ZAMBIA','ZIMBABWE']

# Defining a class to run the server. One per connection. This class will do most of our work.
class IRC_Server:

    # The default constructor - declaring our global variables
    # channel should be rewritten to be a list, which then loops to connect, per channel.
    # This needs to support an alternate nick.
    def __init__(self, host, port, nick, channel , password =""):
        self.irc_host = host
        self.irc_port = port
        self.irc_nick = nick
        self.irc_channel = channel
        self.irc_sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.is_connected = False
        self.should_reconnect = False
        self.command = ""


    # This is the bit that controls connection to a server & channel.
    # It should be rewritten to allow multiple channels in a single server.
    # This needs to have an "auto identify" as part of its script, or support a custom connect message.
    def connect(self):
        self.should_reconnect = True
        try:
            self.irc_sock.connect ((self.irc_host, self.irc_port))
        except:
            print ("Error: Could not connect to IRC; Host: " + str(self.irc_host) + "Port: " + str(self.irc_port))
            exit(1) # We should make it recconect if it gets an error here
        print ("Connected to: " + str(self.irc_host) + ":" + str(self.irc_port))

        str_buff = ("NICK %s \r\n") % (self.irc_nick)
        self.irc_sock.send (str_buff.encode())
        print ("Setting bot nick to " + str(self.irc_nick) )

        str_buff = ("USER %s 8 * :X\r\n") % (self.irc_nick)
        self.irc_sock.send (str_buff.encode())
        print ("Setting User")
        # Insert Alternate nick code here.

        # Insert Auto-Identify code here.

        str_buff = ( "JOIN %s \r\n" ) % (self.irc_channel)
        self.irc_sock.send (str_buff.encode())
        print ("Joining channel " + str(self.irc_channel) )
        self.is_connected = True
        self.listen()
        
    def listen(self):
        while self.is_connected:
            recv = self.irc_sock.recv( 4096 )
            if str(recv).find ( "PING" ) != -1:
                self.irc_sock.send ( "PONG ".encode() + recv.split() [ 1 ] + "\r\n".encode() )
            if str(recv).find ( "PRIVMSG" ) != -1:
                irc_user_nick = str(recv).split ( '!' ) [ 0 ] . split ( ":")[1]
                irc_user_host = str(recv).split ( '@' ) [ 1 ] . split ( ' ' ) [ 0 ]
                irc_user_message = self.data_to_message(str(recv)).encode('utf-8').decode('utf-8')
                irc_user_message = str(irc_user_message)
                suit = re.compile('PRIVMSG')
                if suit.search(irc_user_message):   #for people with ipv6
                    irc_user_message = str(recv).split ( 'PRIVMSG' ) [ 1 ] . split ( ' :') [ 1 ]
                    irc_user_message = irc_user_message[:-5].encode('utf-8').decode('utf-8')
                    irc_user_message = str(irc_user_message)
                print ( irc_user_nick + ": " + irc_user_message)
                # Logs of #openra and openra-dev
                chan = str(recv).split ( 'PRIVMSG' ) [ 1 ] . lstrip() . split(' :')[0]
                if (len(str(irc_user_message)) >= 0):
                    if chan == '#openra' or chan == '#openra-dev':
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
                            real_hours = '0'+hours
                        else:
                            real_hours = hours
                        if len(minutes) == 1:
                            real_minutes = '0'+minutes
                        else:
                            real_minutes = minutes
                        row = '['+real_hours+':'+real_minutes+'] '+irc_user_nick+': '+str(irc_user_message)+'\n'
                        if chan == '#openra':
                            chan_d = 'openra'
                        elif chan == '#openra-dev':
                            chan_d = 'openra-dev'
                        else:
                            chan_d = 'pms'
                        filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                        dir = os.path.dirname(filename)
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        file = open(filename,'a')
                        file.write(row)
                        file.close()
              
                # "!" Indicated a command
                if ( str(irc_user_message[0]) == "!" ):
                    self.command = str(irc_user_message[1:])
                    # (str(recv)).split()[2] ) is simply the channel the command was heard on.
                    self.process_command(irc_user_nick, ( (str(recv)).split()[2] ) )
        if self.should_reconnect:
            self.connect()

    def data_to_message(self,data):
        data = data[data.find(':')+1:len(data)]
        data = data[data.find(':')+1:len(data)]
        data = str(data[0:len(data)-5])
        return data

    # This function sends a message to a channel, which must start with a #.
    def send_message_to_channel(self,data,channel):
        print ( ( "%s: %s") % (self.irc_nick, data) )
        self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % (channel, data)).encode() )

    # This function takes a channel, which must start with a #.
    def join_channel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "JOIN %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())
            # This needs to test if the channel is full
            # This needs to modify the list of active channels

    # This function takes a channel, which must start with a #.
    def quit_channel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "PART %s \r\n" ) % (channel)
            self.irc_sock.send (str_buff.encode())
            # This needs to modify the list of active channels


    # This nice function here runs ALL the commands.
    # For now, we only have 2: root admin, and anyone.
    def process_command(self, user, channel):
        # This line makes sure an actual command was sent, not a plain "!"
        if ( len(self.command.split()) == 0):
            return
        # So the command isn't case sensitive
        command = (self.command).lower()
        # Break the command into pieces, so we can interpret it with arguments
        command = command.split()

        # All admin only commands go in here.
        if (user == root_admin):
            # The first set of commands are ones that don't take parameters
            if ( len(command) == 1):

                #This command shuts the bot down.
                if (command[0] == "quit"):
                    str_buff = ( "QUIT %s \r\n" ) % (channel)
                    self.irc_sock.send (str_buff.encode())
                    self.irc_sock.close()
                    self.is_connected = False
                    self.should_reconnect = False

            # These commands take parameters
            else:

                # This command makes the bot join a channel
                # This needs to be rewritten in a better way, to catch multiple channels
                if (command[0] == "join"):
                    if ( (command[1])[0] == "#"):
                        irc_channel = command[1]
                    else:
                        irc_channel = "#" + command[1]
                    self.join_channel(irc_channel)

                # This command makes the bot part a channel
                # This needs to be rewritten in a better way, to catch multiple channels
                if (command[0] == "part"):
                    if ( (command[1])[0] == "#"):
                        irc_channel = command[1]
                    else:
                        irc_channel = "#" + command[1]
                    self.quit_channel(irc_channel)

        # All public commands go here
        # The first set of commands are ones that don't take parameters
        #########################################################################################
        if ( len(command) > 3):
            if ( command[0] == "translate"):
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
                        os.system("python tr.py")
                        time.sleep(0.5)
                        filename = 'tr.text'
                        file = open(filename, 'r')
                        text = file.readline()
                        file.close()
                        if re.search("^#", channel):
                            self.send_message_to_channel( (text), channel)
                        else:
                            self.send_message_to_channel( (text), user)
        if ( len(command) == 2):
            if (command[0] == "games"):
                os.system("wget http://master.open-ra.org/list.php > /dev/null 2>&1")
                filename = 'list.php'
                file = open(filename, 'r')
                lines = file.readlines()
                file.close()
                os.system("rm list.php")
                length = len(lines)
                if length == 1:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("No games found"), channel)
                    else:
                        self.send_message_to_channel( ("No games found"), user)
                else:   # there are one or more games
                    if (command[1] == "1"):
                        length = length / 9 # number of games
                        a1=2
                        loc=3
                        a2=4
                        a3=5
                        a4=7
                        for i in range(int(length)):
                            if lines[a2].lstrip().rstrip() == 'State: 1':
                                state = '(W)'
                                ### for location
                                ip=lines[loc].split(':')[1].lstrip()    # ip address
                                os.system("whois "+ip+" > whois_info")
                                time.sleep(1)
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
                                games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(25)+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+lines[a4].lstrip().rstrip().split(' ')[1]+' - '+country
                                a1=a1+9
                                loc=loc+9
                                a2=a2+9
                                a3=a3+9
                                a4=a4+9
                                if re.search("^#", channel):
                                    self.send_message_to_channel( (games), channel )
                                else:
                                    self.send_message_to_channel( (games), user )
                    elif (command[1] == "2"):
                        length = length / 9 # number of games
                        a1=2
                        loc=3
                        a2=4
                        a3=5
                        a4=7
                        for i in range(int(length)):
                            if lines[a2].lstrip().rstrip() == 'State: 2':
                                state = '(P)'
                                ### for location
                                ip=lines[loc].split(':')[1].lstrip()    # ip address
                                os.system("whois "+ip+" > whois_info")
                                time.sleep(1)
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
                                games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(25)+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+lines[a4].lstrip().rstrip().split(' ')[1]+' - '+country
                                a1=a1+9
                                loc=loc+9
                                a2=a2+9
                                a3=a3+9
                                a4=a4+9
                                if re.search("^#", channel):
                                    self.send_message_to_channel( (games), channel )
                                else:
                                    self.send_message_to_channel( (games), user )
                    else:   #it is pattern
                        chars=['*','.','$','^','@','{','}','+','?']
                        for i in range(int(len(chars))):
                            if chars[i] in command[1]:
                                check = 'tru'
                                break
                            else:
                                check = 'fals'
                        if check == 'fals':
                            p = re.compile(command[1], re.IGNORECASE)
                            length = length / 9 # number of games
                            a1=2
                            loc=3
                            a2=4
                            a3=5
                            a4=7
                            for i in range(int(length)):
                                if p.search(lines[a1]):
                                    if lines[a2].lstrip().rstrip() == 'State: 1':
                                        state = '(W)'
                                    elif lines[a2].lstrip().rstrip() == 'State: 2':
                                        state = '(P)'
                                    ### for location
                                    ip=lines[loc].split(':')[1].lstrip()    # ip address
                                    os.system("whois "+ip+" > whois_info")
                                    time.sleep(1)
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
                                    games = '@ '+sname.lstrip().rstrip()[6:].lstrip()+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+lines[a4].lstrip().rstrip().split(' ')[1]+' - '+country
                                    if re.search("^#", channel):
                                        self.send_message_to_channel( (games), channel)
                                    else:
                                        self.send_message_to_channel( (games), user)
                                    break
                                a1=a1+9
                                loc=loc+9
                                a2=a2+9
                                a3=a3+9
                                a4=a4+9                 
#        if re.search('http://*', command):
#           length = len(command)
#           for i in range(int(length)):
#               if re.search('http://*', command[i]):
#                   link = command[i]
#                   break
#           os.system("wget "+link)
#           part = len(link.split('//'))        
#           if part == 2:
#               filename = 'index.html'
#               file = open(filename, 'r')
#               lines = file.readlines()
 
        if ( len(command) == 1):

            if (command[0] == "hi"):
                if re.search("^#", channel):
                    self.send_message_to_channel( ("Hello, " + user), channel )
                else:
                    self.send_message_to_channel( ("Hello, " + user), user)
            if (command[0] == "translate"):
                self.send_message_to_channel( ("Usage: !translate <from language> <to language> <text to translate>   |   To get a list of the available languages: !langs   |   For example, to translate from English to German: !translate en de Thank you"), user)
            if (command[0] == "langs"):
                b=0
                for i in range(25):
                    line1 = languages[b].ljust(8)+real_langs[b].ljust(20)
                    b=b+1
                    line2 = languages[b].ljust(8)+real_langs[b].ljust(20)
                    line_output=line1+'| '+line2
                    time.sleep(1)
                    self.send_message_to_channel( (line_output), user)
                    b=b+1
                    if b == 50:
                        break
            if (command[0] == "games"):
                os.system("wget http://master.open-ra.org/list.php > /dev/null 2>&1")
                filename = "list.php"
                file = open(filename, 'r')
                lines = file.readlines()    #got a list
                file.close()
                os.system("rm list.php")
                length = len(lines)
                if length == 1:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("No games found"), channel )
                    else:
                        self.send_message_to_channel( ("No games found"), user )
                else:
                    length = length / 9
                    a1=2
                    loc=3
                    a2=4
                    a3=5
                    a4=7
                    games=''
                    count='0'
                    for i in range(int(length)):
                        if lines[a2].lstrip().rstrip() == 'State: 1':
                            state = '(W)'
                        elif lines[a2].lstrip().rstrip() == 'State: 2':
                            state = '(P)'
                        ### for location
                        ip=lines[loc].split(':')[1].lstrip()    # ip address
                        os.system("whois "+ip+" > whois_info")
                        time.sleep(0.7)
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
                        games = str(i)+': '+sname.lstrip().rstrip()[6:].lstrip().ljust(25)+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+lines[a4].lstrip().rstrip().split(' ')[1]+' - '+country
                        a1=a1+9 
                        loc=loc+9
                        a2=a2+9
                        a3=a3+9
                        a4=a4+9
                        if state == "(W)":
                            count='1'
                            if re.search("^#", channel):
                                self.send_message_to_channel( (games), channel )
                            else:
                                self.send_message_to_channel( (games), user )
                    if count == "0":
                        if re.search("^#", channel):
                            self.send_message_to_channel( ("No games waiting for players found"), channel )
                        else:
                            self.send_message_to_channel( ("No games waiting for players found"), user )
        else:
            if (command[0] == "bop"):
                self.send_message_to_channel( ("\x01ACTION bopz " + str(command[1]) + "\x01"), channel )


# Here begins the main programs flow:

test2 = IRC_Server("irc.freenode.net", 6667, "orabot", "#arma.ctf")
test = IRC_Server("irc.freenode.net", 6667, "orabot", "#openra")
run_test = threading.Thread(None, test.connect)
run_test.start()

while (test.should_reconnect):
    time.sleep(5)
