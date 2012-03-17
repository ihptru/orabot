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

import time
import config
import urllib.request
import json
import os
import sqlite3
import subprocess
import shutil
from libs import pygeoip

def start(self):
    while True:
        prepare(self)
        time.sleep(129600)   #36 hours

def prepare(self):
    try:
        if os.path.exists('db/openra.db'):
            os.remove('db/openra.db')
        url = 'http://master.open-ra.org/db/openra.db'
        remoteFile = subprocess.Popen(['wget', url, '-P', 'db/', '-o', 'var/wget_log']).wait()
    except:
        print("Could not fetch a remote database (openra_stats)")
        return
    
    conn = sqlite3.connect('db/openra.db')
    cur = conn.cursor()

    content_maps = """
    <html>
    <head>
    <title>OpenRA Map's Statistics</title>
    <style type="text/css">
        body {
            font: 12px/16px Verdana, Arial, Helvetica;
        }

        #main {
            font-family: monospace;
            margin: auto;
            padding:auto;
            text-align: center;
            max-width:700px;
        }

        a:visited {
            color: #0000FF;
        }

        a:link {
            color: #0000FF;
        }

        a:hover {
            background-color:#FFFF00;
        }

        table {
            border: 2px solid #0000FF;
        }
        
        td {
            border: 2px solid #0000FF;
            padding: 2px 2px 2px 2px;
        }
        
        .players {
            color: #0000FF;
            text-decoration: underline;
        }
        
        .title {
            color: #ff7800;
        }
        
        .info {
            text-decoration: underline;
        }
        
        img {
            border: 0px;
        }
    </style>
    </head>
    <body>
    <div id="main">
        <h2><u>Mostly played maps</u></h2>
        <i><a href='../serverstats/index.html'>servers' stats</a></i><br>
        <i>last updated %s</i><br><br>
    </div>
    <table id="main">
        <tr>
            <td>minimap</td>
            <td>info</td>
            <td>games</td>
        </tr>
    """ % (time.strftime('%Y-%m-%d'), )

    sql = """SELECT map,count(map) as counts, avg(players) as players FROM servers
                WHERE players > 1 AND state = 2
            GROUP BY map
            ORDER BY counts DESC LIMIT 100
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()
    for i in range(len(records)):
        try:
            url = "http://content.open-ra.org/api/map_data.php?load=%s" % records[i][0]
            data = urllib.request.urlopen(url).read().decode('utf-8')
        except:
            continue
        if ( data.strip() == "-1" ):
            continue
        y = json.loads(data)
        link = y[0]['url']
        minimap = os.path.dirname(y[0]['url']) + "/minimap.bmp"

        url = "http://content.open-ra.org/api/map_data.php?hash=%s" % records[i][0]
        data = urllib.request.urlopen(url).read().decode('utf-8')
        y = json.loads(data)

        if ( y[0]['description'].strip() == "" ):
            desc = "none"
        else:
            desc = y[0]['description']
        content_maps += """
            <tr><td><a href="http://content.open-ra.org/?p=detail&table=maps&id={0}"><img src="{1}" /></a></td>
        """.format(y[0]['id'], minimap)
        content_maps += """
            <td><span class="title">title:</span> {0}<br><span class="title">description:</span> {1}<br><span class="title">author:</span> {2}<br><span class="title">mod:</span> {3}<br><span class="info">This map is played on an average with <span class="players">{4}</span> players</span><br><a href="{5}">download</a></td>
        """.format(y[0]['title'], desc, y[0]['author'], y[0]['mod'], round(float(records[i][2])), link)
        content_maps += """
            <td>{0}</td></tr>
        """.format(records[i][1])

    content_maps += """
    </table>

    </body>
    </html>
    """

    file = open(config.save_stats_path+'mapstats/index.html', 'w')
    file.writelines(content_maps)
    file.close()
    
    # server stats
    content_servers= """
    <html>
    <head>
    <title>OpenRA Servers Statistics</title>
    <style type="text/css">
        body {
            font: 12px/16px Verdana, Arial, Helvetica;
        }

        #main {
            font-family: monospace;
            margin: auto;
            padding:auto;
            text-align: center;
            max-width:700px;
        }

        a:visited {
            color: #0000FF;
        }

        a:link {
            color: #0000FF;
        }

        a:hover {
            background-color:#FFFF00;
        }

        table {
            border: 2px solid #0000FF;
        }
        
        td {
            border: 2px solid #0000FF;
            padding: 2px 2px 2px 2px;
        }
        
        .players {
            color: #0000FF;
            text-decoration: underline;
        }
        
        .title {
            color: #ff7800;
        }
        
        .info {
            text-decoration: underline;
        }
        
        img {
            border: 0px;
        }
    </style>
    </head>
    <body>
    <div id="main">
        <h2><u>Country rating</u></h2>
        <i><a href='../mapstats/index.html'>maps' stats</a></i><br>
        <i>last updated %s</i><br><br>
    </div>
    <table id="main">
        <tr>
            <td style='background-color:#FFFF00;'>country</td>
            <td style='background-color:#FFFF00;'>games</td>
        </tr>
    """ % (time.strftime('%Y-%m-%d'), )

    sql = """SELECT address FROM servers WHERE state = 2
    """
    cur.execute(sql)
    records = cur.fetchall()
    conn.commit()

    addrs = []
    for i in range(len(records)):
        addrs.append(records[i][0].rsplit(':', 1)[0])
    dup = {}
    for ip in addrs:
        dup[ip] = dup.get(ip, 0)+1
    country_dup = {}
    for server in dup:
        gi = pygeoip.GeoIP('libs/pygeoip/GeoIP.dat')
        country = gi.country_name_by_addr(server)   #got country name
        country_dup[country] = country_dup.get(country, 0) + dup[server]
    sorted_country = sorted(country_dup.items(), key=lambda t: t[1])
    sorted_country.reverse()
    for server in sorted_country:
        if server[0].strip() != "":
            content_servers += """<tr><td>%s</td><td>%s</td></tr>
            """ % (server[0], server[1])

    content_servers += """
    </table>

    </body>
    </html>
    """

    file = open(config.save_stats_path+'serverstats/index.html', 'w')
    file.writelines(content_servers)
    file.close()

    shutil.move('db/openra.db', 'var/openra.db')
