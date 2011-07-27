import time
import sqlite3
import urllib.request
import re
from datetime import date

def start(self):
    notify_ip_list = []
    bugreport_var = 0
    while True:
        time.sleep(3)
        bugreport_var = bugreport_var + 1
        ### bugreport part:
        if ( bugreport_var == 2400 ):   #~2 hours
            bugreport_var = 0
            url = 'http://bugs.open-ra.org/projects/openra/issues?set_filter=1&tracker_id=1'
            stream = urllib.request.urlopen(url).read()
            bug_report = stream.split('<td class="tracker">')[1].split('</a>')[0].split('>')[-1].rstrip()
            filename = 'run/bug_report.txt'
            line = ''
            try:
                file = open(filename, 'r')
                line = file.readline()
                file.close()
            except:
                pass
            if ( bug_report != line.rstrip() ):
                filename = 'run/bug_report.txt'
                file = open(filename, 'w')
                file.write(bug_report)
                file.close()
                message = "New Bug Report (http://bugs.open-ra.org): "+bug_report
                self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % ('#openra', message)).encode())
        ### new game notifications part
        ip_current_games = []
        timeouts = ['s','m','h','d']
        url = 'http://master.open-ra.org/list.php'
        stream = urllib.request.urlopen(url).read()
        if ( stream != b'' ):
            split_games = str(stream).split('\\nGame')
            length_games = len(split_games)
            for i in range(int(length_games)):
                ip = split_games[i].split('\\n\\t')[3].split()[1].split(':')[0]
                ip_current_games.append(ip)
                state = split_games[i].split('\\n\\t')[4]
                if ( ip in notify_ip_list ):
                    if ( state == 'State: 2' ):
                        #game in list but started, remove from `notify_ip_list`
                        ip_index = notify_ip_list.index(ip)
                        del notify_ip_list[ip_index]
                        ip_index = ip_current_games.index(ip)
                        del ip_current_games[ip_index]
                else:   #ip is not in a list
                    if ( state == 'State: 1' ):
                        notify_ip_list.append(ip)
                        name = " ".join(split_games[i].split('\\n\\t')[2].split()[1:])
                        mod = split_games[i].split('\\n\\t')[7].split()[1].split('@')[0]
                        try:
                            version = " - version: " + split_games[i].split('\\n\\t')[7].split()[1].split('@')[1]
                        except:
                            version = ''    #no version in output
                        down = name.split('[down]')
                        if ( len(down) == 1 ):  #game is not [down]
                            conn = sqlite3.connect('../db/openra.sqlite')
                            cur = conn.cursor()
                            sql = """SELECT user,date,mod,version,timeout FROM notify
                            """
                            cur.execute(sql)
                            conn.commit()
                            row = []
                            data = []
                            for row in cur:
                                data.append(row)
                            if ( data != [] ):
                                length_data = len(data)
                                for i in range(int(length_data)):
                                    db_user = data[i][0]
                                    db_date = data[i][1]
                                    db_mod = data[i][2]
                                    db_version = data[i][3]
                                    db_timeout = data[i][4]
                                    if ( db_mod.lower() == mod or db_mod.lower() == 'all' ):
                                        if ( re.search(db_version, version) or db_version.lower() == 'all' ):
                                            notify_message = "New game: "+name+" - mod: "+mod+version
                                            if ( db_timeout.lower() == 'all' ):
                                                self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % (db_user, notify_message)).encode() )
                                            elif ( db_timeout.lower() == 'till_quit' ):
                                                self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % (db_user, notify_message)).encode() )
                                            else:
                                                date_of_adding = int(db_date.replace('-',''))
                                                ###
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
                                                seconds = b.split('tm_sec=')[1].split(',')[0]
                                                if len(hours) == 1:
                                                    hours = '0'+hours
                                                else:
                                                    hours = hours
                                                if len(minutes) == 1:
                                                    minutes = '0'+minutes
                                                else:
                                                    minutes = minutes
                                                if len(seconds) == 1:
                                                    seconds = '0'+seconds
                                                else:
                                                    seconds = seconds
                                                localtime = year+month+day+hours+minutes+seconds
                                                localtime = int(localtime)
                                                difference = localtime - date_of_adding     #in result - must be less then timeout
                                                if ( db_timeout[-1] == 's' ):
                                                    timeout = db_timeout[0:-1]
                                                elif ( db_timeout[-1] == 'm' ):
                                                    timeout = int(db_timeout[0:-1]+'00')
                                                elif ( db_timeout[-1] == 'h' ):
                                                    timeout = int(db_timeout[0:-1]+'0000')
                                                elif ( db_timeout[-1] == 'd' ):
                                                    timeout = int(db_timeout[0:-1]+'000000')
                                                if ( difference < timeout ):
                                                    self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % (db_user, notify_message)).encode())
                                                else:   # timeout is over
                                                    sql = """DELETE from notify
                                                            WHERE user = '"""+db_user+"""'
                                                    """
                                                    cur.execute(sql)
                                                    conn.commit()
                                                ###
            length = len(notify_ip_list)
            indexes = []
            for i in range(int(length)):
                if ( notify_ip_list[i] not in ip_current_games ):
                    indexes.append(i)   #indexes to remove from notify_ip_list
            for i in indexes:
                del notify_ip_list[i]
