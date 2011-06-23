#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This code was written for Python 3.1.1

import socket, sys, multiprocessing, time
import os
import re
from datetime import date
import sqlite3
import hashlib
import random

# root admin
root_admin = "ihptru"
root_admin_password = "password" #only for the successful first run, dont forget to remove it later

### UNCOMMENT BELOW ON THE FIRST RUN
                #conn = sqlite3.connect('../db/openra.sqlite')
                #cur = conn.cursor()
                #sql = """CREATE TABLE register (
                #uid int NOT NULL,
                #user varchar(20) NOT NULL,
                #pass varchar(50),
                #owner boolean NOT NULL DEFAULT '0',
                #authenticated boolean NOT NULL DEFAULT '0'
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #
                #user_password = hashlib.md5(root_admin_password.encode('utf-8')).hexdigest()     
                #sql = """INSERT INTO register
                #        (uid,user,pass,owner)
                #        VALUES
                #        (
                #        1,'"""+root_admin+"','"+str(user_password)+"'"+""",1
                #        )       
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE black_list (
                #    uid integer NOT NULL,
                #    user varchar(30) NOT NULL,
                #    date_time date NOT NULL,
                #    count integer NOT NULL
                #    )        
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """INSERT INTO black_list
                #       (uid,user,date_time,count)
                #       VALUES
                #       (
                #       1,'test',strftime('%Y-%m-%d-%H-%M'),1
                #       )
                #"""
                #cur.execute(sql)
                #conn.commit()
                #
                #sql = """CREATE TABLE commands (
                #        uid integer NOT NULL,
                #        user varchar(30) NOT NULL,
                #        command varchar(300) NOT NULL,
                #        date_time date NOT NULL
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #for i in range(31):
                #    sql = """INSERT INTO commands
                #        (uid,user,command,date_time)
                #        VALUES
                #        (
                #        1,'test','test_command',strftime('%Y-%m-%d-%H-%M-%S')
                #        )
                #    """
                #    cur.execute(sql)
                #    conn.commit()
                #sql = """CREATE TABLE users (
                #uid integer NOT NULL,
                #user varchar(30) NOT NULL,
                #date date
                #)               
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql= """INSERT INTO users
                #        (uid,user)
                #        VALUES
                #        (
                #        1,'test'
                #        )
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE later (
                #        uid integer NOT NULL,
                #        sender varchar(30) NOT NULL,
                #        reciever varchar(30) NOT NULL,
                #        channel varchar(30) NOT NULL,
                #        date date NOT NULL,
                #        message varchar(1000) NOT NULL
                #)             
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """INSERT INTO later
                #        (uid,sender,reciever,channel,date,message)
                #        VALUES
                #        (
                #        1,'test','test','#test',strftime('%Y-%m-%d-%H-%M-%S'),'Hello, how are you?'
                #        )                
                #"""
                #cur.execute(sql)
                #conn.commit()
                ###
                #sql = """CREATE TABLE "pickup_1v1" (
                #"uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
                #"name" VARCHAR NOT NULL ,
                #"host" BOOL NOT NULL  DEFAULT 0,
                #"timeout" DATETIME NOT NULL
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE "pickup_2v2" (
                #"uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
                #"name" VARCHAR NOT NULL ,
                #"host" BOOL NOT NULL  DEFAULT 0,
                #"timeout" DATETIME NOT NULL
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE "pickup_3v3" (
                #"uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
                #"name" VARCHAR NOT NULL ,
                #"host" BOOL NOT NULL  DEFAULT 0,
                #"timeout" DATETIME NOT NULL
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE "pickup_4v4 (
                #"uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
                #"name" VARCHAR NOT NULL ,
                #"host" BOOL NOT NULL  DEFAULT 0,
                #"timeout" DATETIME NOT NULL
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE "pickup_game_start" (
                #"uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
                #"team1" VARCHAR NOT NULL ,
                #"team2" VARCHAR NOT NULL ,
                #"type" VARCHAR NOT NULL ,
                #"host" VARCHAR NOT NULL ,
                #"map" VARCHAR NOT NULL ,
                #"time" DATETIME NOT NULL
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE "pickup_maps" (
                #"uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
                #"name" VARCHAR NOT NULL ,
                #"1v1" BOOL NOT NULL ,
                #"2v2" BOOL NOT NULL ,
                #"3v3" BOOL NOT NULL ,
                #"4v4" BOOL NOT NULL ,
                #"5v5" BOOL NOT NULL
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """INSERT INTO "pickup_maps"
                #       (name,1v1,2v2,3v3,4v4,5v5)
                #       VALUES
                #       (
                #       'East vs West',1,1,0,0,0
                #       )
                #"""
                #cur.execute(sql)
                #conn.commit()
                #sql = """CREATE TABLE "pickup_stats" (
                #"uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
                #"name" VARCHAR NOT NULL ,
                #"games" INTEGER NOT NULL  DEFAULT 0,
                #"hosts" INTEGER NOT NULL  DEFAULT 0,
                #"complaints" INTEGER NOT NULL  DEFAULT 0
                #)
                #"""
                #cur.execute(sql)
                #conn.commit()
                #cur.close()
###

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

    ## The destructor - Close socket.
    def __del__(self):
        self.irc_sock.close()

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
            ### for logs
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
            ### for logs end
            if str(recv).find ( "PING" ) != -1:
                self.irc_sock.send ( "PONG ".encode() + recv.split() [ 1 ] + "\r\n".encode() )
            #recover all nicks on channel
            #if str(recv).find ( "353 orabot =" ) != -1:
            #    print (str(recv))
            #    user_nicks = str(recv).split(':')[2].rstrip()
            #    user_nicks = user_nicks.replace('+','').replace('@','')
            #    user_nicks = user_nicks.split(' ')
            #    self.nicks = user_nicks
            if str(recv).find ( "PRIVMSG" ) != -1:
                irc_user_nick = str(recv).split ( '!' ) [ 0 ] . split ( ":")[1]
                irc_user_host = str(recv).split ( '@' ) [ 1 ] . split ( ' ' ) [ 0 ]
                irc_user_message = self.data_to_message(str(recv)).encode('utf-8').decode('utf-8')
                irc_user_message = str(irc_user_message)
                # if PRIVMSG is still in string - message from person with ipv6
                suit = re.compile('PRIVMSG')
                if suit.search(irc_user_message):
                    irc_user_message = str(recv).split ( 'PRIVMSG' ) [ 1 ] . split ( ' :') [ 1 ]
                    irc_user_message = irc_user_message[:-5].encode('utf-8').decode('utf-8')
                    irc_user_message = str(irc_user_message)
                ###logs
                chan = str(recv).split ( 'PRIVMSG' ) [ 1 ] . lstrip() . split(' :')[0]  #channel ex: #openra
                if chan == '#openra' or chan == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+irc_user_nick+': '+str(irc_user_message)+'\n'
                    if chan == '#openra':
                        chan_d = 'openra'
                    elif chan == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                ### logs end
                print ( irc_user_nick + ": " + irc_user_message)
                # "]" Indicated a command
                if ( str(irc_user_message[0]) == "]" ):
                    self.command = str(irc_user_message[1:])
                    # (str(recv)).split()[2] ) is simply the channel the command was heard on.
                    self.process_command(irc_user_nick, ( (str(recv)).split()[2] ))
### when message cotains link to youtube, show video title
                if re.search('http://www.youtube.com/watch*', str(irc_user_message)) or re.search('http://youtube.com/watch*', str(irc_user_message)):
                    if re.search("^#", chan):
                        link = str(irc_user_message).split('http://')[1].split()[0].split('&')[0]
                        dl_file = link.split('/')[1]
                        link = 'http://'+link
                        os.system("wget "+link+" > /dev/null 2>&1")
                        filename = dl_file
                        file = open(filename, 'r')
                        lines = file.readlines()
                        file.close()
                        os.remove(dl_file)
                        try:
                            video_title = lines[25].split('&#x202a;')[1].split('&#x202c;')[0].replace('&#39;', '\'')
                            self.send_message_to_channel( ("Youtube: "+video_title), chan )
                        except:
                            pass    #video is removed or something
            if str(recv).find ( "JOIN" ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                print (str(recv))
                irc_join_nick = str(recv).split( '!' ) [ 0 ].split( ':' ) [ 1 ]
                irc_join_host = str(recv).split( '!' ) [ 1 ].split( ' ' ) [ 0 ]
                chan = str(recv).split( "JOIN" ) [ 1 ].lstrip().split( ":" )[1].rstrip()     #channle ex: #openra

                sql = """SELECT * FROM users
                        WHERE user = '"""+irc_join_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if irc_join_nick not in row:     #user NOT found, add him (if user is not in db, he could not have ]later message)
                    #get last uid
                    sql = """SELECT * FROM users
                            ORDER BY uid DESC LIMIT 1
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    uid_users = row[0]
                    uid_users = uid_users + 1   # uid + 1
                    sql = """INSERT INTO users
                            (uid,user)
                            VALUES
                            (
                            """+str(uid_users)+",'"+str(irc_join_nick)+"'"+"""
                            )
                    """
                    cur.execute(sql)
                    conn.commit()
                else:   #he can have ]later messages
                    sql = """SELECT reciever FROM later
                            WHERE reciever = '"""+irc_join_nick+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()

                    row = []
                    for row in cur:
                        pass
                    if irc_join_nick in row:    #he has messages in database, read it
                        sql = """SELECT * FROM later
                                WHERE reciever = '"""+irc_join_nick+"'"+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                        row = []
                        msgs = []
                        for row in cur:
                            msgs.append(row)
                        msgs_length = len(msgs) #number of messages for player
                        self.send_message_to_channel( ("You have "+str(msgs_length)+" offline messages:"), irc_join_nick )
                        for i in range(int(msgs_length)):
                            who_sent = msgs[i][1]
                            on_channel = msgs[i][3]
                            message_date = msgs[i][4]
                            offline_message = msgs[i][5]
                            self.send_message_to_channel( ("### From: "+who_sent+";  channel: "+on_channel+";  date: "+message_date), irc_join_nick )
                            self.send_message_to_channel( (offline_message.replace("~qq~","'")), irc_join_nick )
                        time.sleep(0.1)
                        sql = """DELETE FROM later
                                WHERE reciever = '"""+irc_join_nick+"'"+"""
                        
                        """
                        
                        cur.execute(sql)
                        conn.commit()
                    #sql = """UPDATE users
                    #        SET date = ''
                    #        WHERE user = '"""+irc_join_nick+"'"+"""
                    #"""
                    #cur.execute(sql)
                    #conn.commit()
                    cur.close()
                ###logs
                if self.irc_channel == '#openra' or self.irc_channel == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+'* '+irc_join_nick+' ('+irc_join_host+') has joined '+self.irc_channel+'\n'
                    if self.irc_channel == '#openra':
                        chan_d = 'openra'
                    elif self.irc_channel == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                ###
            if str(recv).find ( "QUIT" ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                print (str(recv))
                irc_quit_nick = str(recv).split( "!" )[ 0 ].split( ":" ) [ 1 ]
                irc_quit_message = str(recv).split('QUIT :')[1].rstrip()
                #change authenticated status
                sql = """SELECT * FROM register
                        WHERE user = '"""+irc_quit_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if irc_quit_nick in row:
                    authenticated = row[4]
                    if authenticated == 1:
                        sql = """UPDATE register
                                SET authenticated = 0
                                WHERE user = '"""+irc_quit_nick+"'"+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                ### for ]last              
                sql = """UPDATE users
                        SET date = strftime('%Y-%m-%d-%H-%M-%S')
                        WHERE user = '"""+str(irc_quit_nick)+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                cur.close()
                ### for ]pick
                modes = ['1v1','2v2','3v3','4v4']
                diff_mode = ''
                for diff_mode in modes:
                    sql = """DELETE FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+irc_quit_nick+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                ##logs
                if self.irc_channel == '#openra' or self.irc_channel == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+'* '+irc_quit_nick+' has quit ('+irc_quit_message.rstrip()+')\n'
                    if self.irc_channel == '#openra':
                        chan_d = 'openra'
                    elif self.irc_channel == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
            if str(recv).find ( "PART" ) != -1:
                conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
                cur=conn.cursor()
                print (str(recv))
                irc_part_nick = str(recv).split( "!" )[ 0 ].split( ":" ) [ 1 ]
                ###logout
                sql = """SELECT * FROM register
                        WHERE user = '"""+irc_part_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                for row in cur:
                    pass
                if irc_part_nick in row:
                    authenticated = row[4]
                    if authenticated == 1:
                        sql = """UPDATE register
                                SET authenticated = 0
                                WHERE user = '"""+irc_part_nick+"'"+"""
                        """
                        cur.execute(sql)
                        conn.commit()
                ### for ]last              
                sql = """UPDATE users
                        SET date = strftime('%Y-%m-%d-%H-%M-%S')
                        WHERE user = '"""+str(irc_part_nick)+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                cur.close()
                ### for ]pick
                modes = ['1v1','2v2','3v3','4v4']
                diff_mode = ''
                for diff_mode in modes:
                    sql = """DELETE FROM pickup_"""+diff_mode+"""
                            WHERE name = '"""+irc_part_nick+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                ###logs
                if self.irc_channel == '#openra' or self.irc_channel == '#openra-dev':
                    row = '['+real_hours+':'+real_minutes+'] '+'* '+irc_part_nick+' has left '+chan+'\n'
                    if self.irc_channel == '#openra':
                        chan_d = 'openra'
                    elif self.irc_channel == '#openra-dev':
                        chan_d = 'openra-dev'
                    else:
                        chan_d = 'trash'
                    filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
                    dir = os.path.dirname(filename)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    file = open(filename,'a')
                    file.write(row)
                    file.close()
                ###
                
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
        ### for logs
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
        if channel == '#openra' or channel == '#openra-dev':
            row = '['+real_hours+':'+real_minutes+'] '+self.irc_nick+': '+str(data)+'\n'
            if channel == '#openra':
                chan_d = 'openra'
            elif channel == '#openra-dev':
                chan_d = 'openra-dev'
            else:
                chan_d = 'trash'
            filename = '/var/openra/irc/logs/'+chan_d+'/'+year+'/'+month+'/'+day
            dir = os.path.dirname(filename)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file = open(filename,'a')
            file.write(row)
            file.close()
        ### for logs end
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
            error = "Usage: ]command [arguments]"
            if re.search("^#", channel):
                self.send_message_to_channel( (error), channel)
            else:
                self.send_message_to_channel( (error), user)
            return
        # So the command isn't case sensitive
        command = (self.command)
        # Break the command into pieces, so we can interpret it with arguments
        command = command.split()
        string_command = " ".join(command)

### START OF SPAM FILTER
        conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
        cur=conn.cursor()
        sql = """SELECT * FROM black_list
            WHERE user = '"""+user+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
        
        row = []
        for row in cur:
            pass
        check_ignore = '0'
        if user in row:
            ignore_count = row[3]
            ignore_minutes = str(ignore_count)+'0'
            ignore_date = "".join(str(row[2]).split('-'))
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
            difference = int(localtime) - int(ignore_date)  #how many minutes after last ignore
            if int(difference) < int(ignore_minutes):
                check_ignore = '1'  #lock, start ignore
            else:   #no need to ignore, ignore_minutes < difference
                check_ignore = '0'
        if check_ignore == '0':
            #get last uid_commands
            sql = """SELECT * FROM commands
                    ORDER BY uid DESC LIMIT 1
            """
            cur.execute(sql)
            conn.commit()
            
            for row in cur:
                pass
            uid_commands=row[0]
            
            uid_commands = uid_commands + 1
            #clear 'commands' table after each 1 000 000 record
            if uid_commands >= 1000:
                uid_commands = 1
                sql = """DELETE FROM commands WHERE uid > 1"""
                cur.execute(sql)
                conn.commit()
    
            #write each command into 'commands' table 
            sql = """INSERT INTO commands
                    (uid,user,command,date_time)
                    VALUES
                    (
                    """+str(uid_commands)+",'"+str(user)+"','"+string_command.replace("'","~qq~")+"',"+"strftime('%Y-%m-%d-%H-%M-%S')"+""" 
                    )        
            """
            cur.execute(sql)
            conn.commit()
            
            #extract last 30 records
            sql = """SELECT * FROM commands
                ORDER BY uid DESC LIMIT 30
            """
            cur.execute(sql)
            
        
            var=[]
            for row in cur:
                var.append(row)
            var.reverse()
            actual=[]
            user_data=[]
            for i in range(30):
                if user in str(var[i][1]):
                    actual.append(str(var[i][1]))   #name
                    actual.append(str(var[i][3]))   #date and time
                    user_data.append(actual)
                    actual=[]
            user_data_length = len(user_data)
            if user_data_length > 10:
                #get player's (last - 10) record
                user_data_len10 = user_data_length - 10
                actual=user_data[user_data_len10]
                first_date="".join(actual[1].split('-'))    #date and time of last - 10 record
                last_date="".join(user_data[user_data_length-1][1].split('-'))  #current date/time
                seconds_range=int(last_date)-int(first_date)  #how many seconds between player's commands
                if seconds_range < 30:  #player made more then 10 commands in range of 30 seconds. It is too quick, spam!
                    sql = """SELECT * FROM black_list
                            WHERE user = '"""+user+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()

                    row = []
                    for row in cur:
                        pass
                    if user not in row:   #user does not exist in 'black_list' table yet
                        #get last uid_black_list

                        sql = """SELECT * FROM black_list
                                ORDER BY uid DESC LIMIT 1
                        """
                        cur.execute(sql)
                        conn.commit()
       
                        for row in cur:
                            pass
                        uid_black_list=row[0]
                        uid_black_list = uid_black_list + 1
                        
                        sql = """INSERT INTO black_list
                            (uid,user,date_time,count)
                            VALUES
                            (
                            """+str(uid_black_list)+",'"+user+"',strftime('%Y-%m-%d-%H-%M'),"+str(1)+"""
                            )                   
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:   #in row : exists in 'black_table'
                        count_ignore = row[3]
                        count_ignore = count_ignore + 1
                        sql = """UPDATE black_list
                                SET count = """+str(count_ignore)+", "+"""date_time = strftime('%Y-%m-%d-%H-%M')
                                WHERE user = '"""+user+"'"+""" 
                        """
                        cur.execute(sql)
                        conn.commit()
                    sql = """SELECT * FROM black_list
                        WHERE user = '"""+user+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()

                    row = []
                    for row in cur:
                        pass
                    if user in row:
                        ignore_count = row[3]
                        ignore_minutes = str(ignore_count)+'0'
                        check_ignore = '1'  #lock, start ignore        
                        if re.search("^#", channel):
                            self.send_message_to_channel( (user+", your actions are counted as spam, I will ignore you for "+str(ignore_minutes)+" minutes"), channel )
                        else:
                            self.send_message_to_channel( (user+", your actions are counted as spam, I will ignore you for "+str(ignore_minutes)+" minutes"), user )
                        return
### END OF SPAM FILTER
############    COMMADS:
            ### check if user is registered for privileged commands
            sql = """SELECT * FROM register
                    WHERE user = '"""+user+"'"+"""
            """
            cur.execute(sql)
            conn.commit()
            row = []
            for row in cur:
                pass
            if user in row:     #user exists in 'register' table
                owner = row[3]
                authenticated = row[4]
                if (authenticated == 1):    #he is also authenticated           
                    ### All admin only commands go in here.
                    if ( command[0].lower() == "quit" ):
                        if ( len(command) == 1 ):
                            str_buff = ( "QUIT %s \r\n" ) % (channel)
                            self.irc_sock.send (str_buff.encode())
                            self.irc_sock.close()
                            self.is_connected = False
                            self.should_reconnect = False
                    if ( command[0].lower() == "log" ):
                        if ( len(command) == 1 ):
                            if not re.search("^#", channel):
                                sql = """SELECT * FROM commands
                                        ORDER BY uid DESC LIMIT 10
                                """
                                cur.execute(sql)
                                conn.commit()
                                row = []
                                logs = []
                                actual = []
                                for row in cur:
                                    logs.append(row)
                                for i in range(int(len(logs))):
                                    actual.append(logs[i][1])
                                    actual.append(logs[i][2])
                                    actual.append(logs[i][3])
                                    self.send_message_to_channel( ("User: "+actual[0]+"; Date: "+actual[2]+"; Command: ]"+actual[1].replace("~qq~","'")), user)
                                    actual = []
                                    time.sleep(0.5)
                            else:
                                self.send_message_to_channel( ("]log can't be used on a channel"), channel)
                    if ( command[0].lower() == "add" ):
                        if ( len(command) == 2 ):
                            nick = command[1]
                            sql = """SELECT * FROM users
                                    ORDER BY uid DESC LIMIT 1
                            """
                            cur.execute(sql)
                            conn.commit()
                            for row in cur:
                                pass
                            uid_users=row[0]
                            uid_users = uid_users + 1
                            
                            sql = """SELECT * FROM users
                                    WHERE user = '"""+nick+"'"+"""
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            for row in cur:
                                pass
                            if nick in row: #users exists in database already
                                if re.search("^#", channel):
                                    self.send_message_to_channel( ("Error! User already exists"), channel)
                                else:
                                    self.send_message_to_channel( ("Error! User already exists"), user)
                            else:   
                                sql = """INSERT INTO users
                                    (uid,user)
                                    VALUES
                                    (
                                    """+str(uid_users)+",'"+nick+"'"+"""
                                    )
                                """
                                cur.execute(sql)
                                conn.commit()
                                if re.search("^#", channel):
                                    self.send_message_to_channel( ("Confirmed"), channel)
                                else:
                                    self.send_message_to_channel( ("Confirmed"), user)
                        else:
                            if re.search("^#", channel):
                                self.send_message_to_channel( ("Error, wrong request"), channel )
                            else:
                                self.send_message_to_channel( ("Error, wrong request"), user )
                    if ( command[0].lower() == "join" ):
                        if ( len(command) == 2 ):
                            if ( (command[1])[0] == "#"):
                                irc_channel = command[1]
                            else:
                                irc_channel = "#" + command[1]
                            self.join_channel(irc_channel)
                    if ( command[0].lower() == "part" ):
                        if ( len(command) == 2 ):
                            if ( (command[1])[0] == "#"):
                                irc_channel = command[1]
                            else:
                                irc_channel = "#" + command[1]
                            self.quit_channel(irc_channel)
                    if ( command[0].lower() == "complain" ):
                        if ( len(command) == 2 ):
                            name = command[1]
                            sql = """SELECT name,complaints FROM pickup_stats
                                    WHERE name = '"""+name+"""'
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            for row in cur:
                                pass
                            if name not in row:
                                message = "No such a user"
                                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                                self.irc_sock.send (str_buff.encode())
                            else:
                                complaints = row[1]
                                complaints = str(int(complaints) + 1)
                                sql = """UPDATE pickup_stats
                                        SET complaints = """+complaints+"""
                                        WHERE name = '"""+name+"""'
                                """
                                cur.execute(sql)
                                conn.commit()
                                message = "Amount of "+name+"'s complaints increased by 1"
                                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                                self.irc_sock.send (str_buff.encode())
                        else:
                            if re.search("^#", channel):
                                self.send_message_to_channel( ("Error, wrong request"), channel )
                            else:
                                self.send_message_to_channel( ("Error, wrong request"), user )
                    if ( command[0].lower() == "register" ):      #owner command to allow users register
                        if ( len(command) == 2 ):
                            if ( owner == 1 ):
                                if not re.search("^#", channel):    #owner commands only in private
                                    register_nick = command[1]
                                    sql = """SELECT * FROM register
                                            WHERE user = '"""+register_nick+"'"+"""
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    row = []
                                    for row in cur:
                                        pass
                                    if register_nick in row:
                                        self.send_message_to_channel( ("User "+register_nick+" already exists"), user)
                                    else:
                                        sql = """SELECT * FROM register
                                                ORDER BY uid DESC LIMIT 1                                       
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                        row = []
                                        for row in cur:
                                            pass
                                        uid_register = row[0]
                                        uid_register = uid_register + 1
                                        sql = """INSERT INTO register
                                                (uid,user)
                                                VALUES
                                                (
                                                """+str(uid_register)+",'"+register_nick+"'"+"""
                                                )
                                        """
                                        cur.execute(sql)
                                        conn.commit()
                                        self.send_message_to_channel( ("User "+register_nick+" added successfully, he can use ]register to set up a password"), user)
    
            ### All public commands go here
            #########################################################################################
            if ( command[0].lower() == "games" ):
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
                                    games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(25)+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                                    if re.search("^#", channel):
                                        self.send_message_to_channel( (games), channel )
                                    else:
                                        self.send_message_to_channel( (games), user )
                                a1=a1+9 
                                loc=loc+9
                                a2=a2+9
                                a3=a3+9
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
                            if ( command[1] == "1" ):   #request games in State = 1
                                length = length / 9 # number of games
                                a1=2    #name
                                loc=3   #ip
                                a2=4    #state
                                a3=5    #players
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
                                        games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(25)+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                                        if re.search("^#", channel):
                                            self.send_message_to_channel( (games), channel )
                                        else:
                                            self.send_message_to_channel( (games), user )
                                    a1=a1+9
                                    loc=loc+9
                                    a2=a2+9
                                    a3=a3+9
                                    a4=a4+9
                                if ( count == "0" ):
                                    if re.search("^#", channel):
                                        self.send_message_to_channel( ("No games waiting for players found"), channel )
                                    else:
                                        self.send_message_to_channel( ("No games waiting for players found"), user )           
                            elif ( command[1] == "2" ):     # request games in State = 2
                                length = length / 9 # number of games
                                a1=2    #name
                                loc=3   #ip
                                a2=4    #state
                                a3=5    #players
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
                                        games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(25)+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                                        if re.search("^#", channel):
                                            self.send_message_to_channel( (games), channel )
                                        else:
                                            self.send_message_to_channel( (games), user )
                                    a1=a1+9
                                    loc=loc+9
                                    a2=a2+9
                                    a3=a3+9
                                    a4=a4+9
                                if ( count == "0" ):    #appeared no games in State: 2
                                    if re.search("^#", channel):
                                        self.send_message_to_channel( ("No started games found"), channel )
                                    else:
                                        self.send_message_to_channel( ("No started games found"), user )
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
                                            games = '@ '+sname.lstrip().rstrip()[6:].lstrip().ljust(25)+' - '+state+' - '+lines[a3].lstrip().rstrip()+' - '+(lines[a4].lstrip().rstrip().split(' ')[1].split('@')[0].upper()+'@'+ lines[a4].lstrip().rstrip().split(' ')[1].split('@')[1]).ljust(20)+' - '+country
                                            if re.search("^#", channel):
                                                self.send_message_to_channel( (games), channel)
                                            else:
                                                self.send_message_to_channel( (games), user)
                                        a1=a1+9
                                        loc=loc+9
                                        a2=a2+9
                                        a3=a3+9
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
            if ( command[0].lower() == "version" ):
                if ( len(command) == 1 ):
                    os.system("python ../version.py")
                    filename = 'version'
                    file = open(filename, 'r')
                    line = file.readline()
                    file.close()
                    os.remove('version')
                    if ( int(line.split()[0].split('.')[0]) < int(line.split()[1].split('.')[0]) ):
                        newer = 'playtest is newer then release'
                    else:
                        newer = 'release is newer then playtest'
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("Latest release: "+line[0:4]+""+line[4:8]+" | Latest playtest: "+line[9:13]+""+line[13:17]+" | "+newer), channel )
                    else:
                        self.send_message_to_channel( ("Latest release: "+line[0:4]+""+line[4:8]+" | Latest playtest: "+line[9:13]+""+line[13:17]+" | "+newer), user )
                else:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("Error, wrong request"), channel )
                    else:
                        self.send_message_to_channel( ("Error, wrong request"), user )
            if ( command[0].lower() == "ana" ):
                if ( len(command) > 1 ):
                    word = " ".join(command[1:])
                    os.system("python ../ana.py "+word)
                    filename = 'anagram.txt'
                    file = open(filename, 'r')
                    w_choice = file.readline()
                    file.close()
                    if re.search("^#", channel):
                        self.send_message_to_channel( (w_choice), channel)
                    else:
                        self.send_message_to_channel( (w_choice), user)
                else:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("You must specify some text"), channel )
                    else:
                        self.send_message_to_channel( ("You must specify some text"), user )
            if ( command[0].lower() == "help" ):
                if ( len(command) == 1 ):
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("Help: https://github.com/ihptru/orabot/wiki"), channel )
                    else:
                        self.send_message_to_channel( ("Help: https://github.com/ihptru/orabot/wiki"), user )
                else:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("I don't know anything about '"+" ".join(command[1:])+"'"), channel )
                    else:
                        self.send_message_to_channel( ("I don't know anything about '"+" ".join(command[1:])+"'"), user )
            if ( command[0].lower() == "hi" ):
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
            if ( command[0].lower() == "randomteam" ):
                if ( len(command) > 3 ):
                    team_names = " ".join(command[1:])
                    os.system("python ../pyrand.py "+team_names)
                    filename = 'pyrand.txt'
                    file = open(filename, 'r')
                    result_pyrand = file.readline()
                    file.close()
                    if re.search("^#", channel):
                        self.send_message_to_channel( (result_pyrand.rstrip()), channel)
                    else:
                        self.send_message_to_channel( (result_pyrand.rstrip()), user)
                else:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("You must specify at least 3 teams"), channel)
                    else:
                        self.send_message_to_channel( ("You must specify at least 3 teams"), user)
            if ( command[0].lower() == "tr" ):
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
            if ( command[0].lower() == "lang" ):
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
            if ( command[0].lower() == "later" ):
                if ( len(command) > 2 ):
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
                                print (str(recv))
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
            if ( command[0].lower() == "last" ):
                if ( len(command) == 2 ):
                    if re.search("^#", channel):
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
                            if last_time == None:
                                self.send_message_to_channel( ("User is online!"), channel)
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
            if ( command[0].lower() == "register" ):
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
            if ( command[0].lower() == "login" ):
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
            if ( command[0].lower() == "online"):
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
            if ( command[0].lower() == "if" ):
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
                    if ( nick not in row ):
                        if re.search("^#", channel):
                            self.send_message_to_channel( ("False"), channel)
                        else:
                            self.send_message_to_channel( ("False"), user)
                    else:
                        if re.search("^#", channel):
                            self.send_message_to_channel( ("True"), channel)
                        else:
                            self.send_message_to_channel( ("True"), user)
                else:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("Error, wrong request"), channel )
                    else:
                        self.send_message_to_channel( ("Error, wrong request"), user )
            if ( command[0].lower() == "add" ):
                if ( len(command) == 2 ):
                    sql = """SELECT * FROM register
                            WHERE user = '"""+user+"'"+"""
                    """
                    cur.execute(sql)
                    conn.commit()
                    row = []
                    for row in cur:
                        pass
                    if user in row:
                        if row[4] == 0:
                            if re.search("^#", channel):
                                self.send_message_to_channel( ("You are not authenticated"), channel)
                            else:
                                self.send_message_to_channel( ("You are not authenticated"), user)
                    else:
                        if re.search("^#", channel):
                            self.send_message_to_channel( ("Your don't have permissions for this command"), channel)
                        else:
                            self.send_message_to_channel( ("Your don't have permissions for this command"), user)
                else:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("Error, wrong request"), channel )
                    else:
                        self.send_message_to_channel( ("Error, wrong request"), user )
            if ( command[0].lower() == "pick" ):
                if ( len(command) >= 2 ):
                    if re.search("^#", channel):
                        ### ADD ###
                        if ( command[1].lower() == "add" ):
                            if ( len(command) > 2 ) and ( len(command) < 5 ):   #normal about of arguments
                                modes = ['1v1','2v2','3v3','4v4']
                                if ( command[2] not in modes ):
                                    self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                                    return
                                else:
                                    host = '0'
                                    if ( len(command) == 4 ):
                                        if ( command[3] == 'host' ):
                                            host = '1'  #user can host a game
                                        else:
                                            self.send_message_to_channel( ("What is '"+command[3]+"'? Try again"), channel )
                                            return
                                    if ( command[2] == '1v1' ):
                                        amount_players_required = 2
                                    elif ( command[2] == '2v2' ):
                                        amount_players_required = 4
                                    elif ( command[2] == '3v3' ):
                                        amount_players_required = 6
                                    elif ( command[2] == '4v4' ):
                                        amount_players_required = 8
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
                                        if ( int(num_complaints) > 100 ):
                                            self.send_message_to_channel( ("You have too many complaints, please contact more privileged user to figure out this issue"), channel )
                                            return
                                    mode = command[2]
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
                                            self.send_message_to_channel( ("@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(list(team1))+" || Team 2: "+", ".join(list(team2))), channel )
                                            team = team1+team2
                                            name = ''
                                            for name in team:
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
                                                self.send_message_to_channel( ("@ "+mode+" || Hoster: "+hoster+" || Map: "+map_to_play+" || Team 1: "+", ".join(list(team1))+" || Team 2: "+", ".join(list(team2))), channel )
                                                team = team1+team2
                                                name = ''
                                                for name in team:
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
                        if ( command[1].lower() == "lastgame" ):
                            if ( len(command) >= 2 ) and ( len(command) < 4 ):
                                if ( len(command) == 2 ):
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
                                    modes = ['1v1','2v2','3v3','4v4']
                                    if command[2] in modes:
                                        mode = command[2]
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
                        if ( command[1].lower() == "remove" ):
                            if ( len(command) >= 2 ) and ( len(command) < 4 ):
                                modes = ['1v1','2v2','3v3','4v4']
                                if ( len(command) == 2 ):
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
                                    if command[2] in modes:
                                        mode = command[2]
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
                        if ( command[1].lower() == "who" ):
                            if ( len(command) >= 2 ) and ( len(command) < 4 ):
                                modes = ['1v1','2v2','3v3','4v4']
                                if ( len(command) == 2 ):
                                    temp_mode = ''
                                    names = []
                                    for temp_mode in modes:
                                        if ( temp_mode == '1v1' ):
                                            amount_players_required = 2
                                        elif ( temp_mode == '2v2' ):
                                            amount_players_required = 4
                                        elif ( temp_mode == '3v3' ):
                                            amount_players_required = 6
                                        elif ( temp_mode == '4v4' ):
                                            amount_players_required = 8
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
                                    if command[2] in modes:
                                        mode = command[2]
                                        if ( mode == '1v1' ):
                                            amount_players_required = 2
                                        elif ( mode == '2v2' ):
                                            amount_players_required = 4
                                        elif ( mode == '3v3' ):
                                            amount_players_required = 6
                                        elif ( mode == '4v4' ):
                                            amount_players_required = 8
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
                        if ( command[1].lower() == "promote" ):
                            if ( len(command) == 3 ):
                                modes = ['1v1','2v2','3v3','4v4']
                                mode = command[2]
                                if mode in modes:
                                    if ( mode == '1v1' ):
                                        amount_players_required = 2
                                    elif ( mode == '2v2' ):
                                        amount_players_required = 4
                                    elif ( mode == '3v3' ):
                                        amount_players_required = 6
                                    elif ( mode == '4v4' ):
                                        amount_players_required = 8
                                    sql = """SELECT name FROM pickup_"""+mode+"""
                                    """
                                    cur.execute(sql)
                                    conn.commit()
                                    row = []
                                    name = []
                                    for row in cur:
                                        name.append(row[0])
                                    message = "Please add up for :: "+mode+" :: ! "+ str(amount_players_required-int(len(name))) + " more people needed! (Type ]pick add "+mode+")"
                                    self.send_message_to_channel( (message), channel )
                                else:
                                    self.send_message_to_channel( ("Invalid game mode! Try again"), channel )
                                    return
                            else:
                                message = "Specify mode type to promote! 1v1, 2v2, 3v3 or 4v4"
                                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                                self.irc_sock.send (str_buff.encode())

                    else:
                        self.send_message_to_channel( ("]pick * can be used only on a channel"), user )
                else:
                    if re.search("^#", channel):
                        self.send_message_to_channel( ("Error, wrong request"), channel )
                    else:
                        self.send_message_to_channel( ("Error, wrong request"), user )
                            
                    
        
        cur.close()

#####
class BotCrashed(Exception): # Raised if the bot has crashed.
    pass

def main():
    # Here begins the main programs flow:
    test2 = IRC_Server("irc.freenode.net", 6667, "orabot", "#openra")
    test = IRC_Server("irc.freenode.net", 6667, "orabot", "##untitled")
    run_test = multiprocessing.Process(None,test.connect,name="IRC Server" )
    run_test.start()
    try:
        while(test.should_reconnect):
            time.sleep(5)
        run_test.join()
    except KeyboardInterrupt: # Ctrl + C pressed
        pass # We're ignoring that Exception, so the user does not see that this Exception was raised.
    if run_test.is_alive:
        run_test.terminate()
        run_test.join() # Wait for terminate
    if run_test.exitcode == 0 or run_test.exitcode < 0:
        print("Bot exited.")
    else:
        raise BotCrashed("The bot has crashed")
