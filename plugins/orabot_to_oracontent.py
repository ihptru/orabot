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

import config
import sqlite3
import oursql
import time
import os

def start(self):
    while True:
        prepare(self)
        time.sleep(133200)   #37 hours

def prepare(self):
    try:
        if not os.path.exists('var/openra.db'):
            url = 'http://master.open-ra.org/db/openra.db'
            remoteFile = subprocess.Popen(['wget', url, '-P', 'var/', '-o', 'var/wget_log']).wait()
    except:
        print("Could not fetch a remote database (orabot_to_oracontent)")
        return

    mysql_conn = oursql.connect(host=config.content_my_host, user=config.content_my_username, passwd=config.content_my_password, db=config.content_my_database, port=3307)
    sqlite_conn = sqlite3.connect(config.content_sqlite3_path)
    mysql_cur = mysql_conn.cursor()
    sqlite_cur = sqlite_conn.cursor()
    
    sql = """SELECT
                    map,
                    count(map) as counts,
                    avg(players) as players
                FROM servers
                    WHERE players > 1 AND state = 2
                GROUP BY map
                    ORDER BY counts DESC
    """
    sqlite_cur.execute(sql)
    sqlite_data = sqlite_cur.fetchall()
    sqlite_conn.commit()
        
    sql = """SELECT
                    map_hash,
                    amount_games,
                    avg_players
                FROM
                    map_stats
    """
    mysql_cur.execute(sql)
    mysql_data = mysql_cur.fetchall()
    mysql_conn.commit()
        
    list_of_hashes = []
    for i in range(len(mysql_data)):
        list_of_hashes.append(mysql_data[i][0])

    for i in range(len(sqlite_data)):
        if sqlite_data[i][0] in list_of_hashes:
            sql = """UPDATE map_stats
                            SET amount_games = {0}, avg_players = '{1}'
                            WHERE map_hash = '{2}'
            """.format(sqlite_data[i][1], sqlite_data[i][2], sqlite_data[i][0])
            mysql_cur.execute(sql)
            mysql_conn.commit()
        else:
            sql = """INSERT INTO map_stats
                        (map_hash,amount_games,avg_players)
                        VALUES
                        (
                        '{0}',{1},'{2}'
                        )
            """.format(sqlite_data[i][0], sqlite_data[i][1], sqlite_data[i][2])
            mysql_cur.execute(sql)
            mysql_conn.commit()
