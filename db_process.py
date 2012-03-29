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

def start(self):
    conn, cur = self.db_data()
    print(("[%s] Creating databases") % (self.irc_host))
    
    black_list(conn, cur)
    commands(conn, cur)
    users(conn, cur)
    user_channel(conn, cur)
    later(conn, cur)
    pickup(conn, cur)
    notify(conn, cur)
    user_notified(conn,  cur)
    faq(conn, cur)
    pingme(conn, cur)
    commits(conn, cur)
    bugs(conn, cur)
    activity(conn, cur)
    messages(conn, cur)
    games(conn, cur)

    cur.close()
    print(("[%s] Creating databases completed.\tOK") % (self.irc_host))
    
def black_list(conn, cur):
    sql = """CREATE TABLE black_list (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        "user" varchar(30) NOT NULL,
        "date_time" date NOT NULL,
        "count" integer NOT NULL
        )        
    """
    cur.execute(sql)
    conn.commit()

def commands(conn, cur):
    sql = """CREATE TABLE commands (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        "user" varchar(30) NOT NULL,
        "command" varchar(300) NOT NULL,
        "date_time" date NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    for i in range(31):
        sql = """INSERT INTO commands
            (user,command,date_time)
            VALUES
            (
            'test','test_command',strftime('%Y-%m-%d-%H-%M-%S')
            )
        """
        cur.execute(sql)
        conn.commit()
    
def users(conn, cur):
    sql = """CREATE TABLE users (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        "user" varchar(30) NOT NULL,
        "date" date,
        "state" bool NOT NULL DEFAULT 0
        )
    """
    cur.execute(sql)
    conn.commit()

def user_channel(conn, cur):
    sql = """CREATE TABLE user_channel (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        "user" VARCHAR NOT NULL,
        "channel" VARCHAR NOT NULL,
        "status" VARCHAR
        )
    """
    cur.execute(sql)
    conn.commit()

def later(conn, cur):
    sql = """CREATE TABLE later (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        "sender" varchar(30) NOT NULL,
        "reciever" varchar(30) NOT NULL,
        "channel" varchar(30) NOT NULL,
        "date" date NOT NULL,
        "message" varchar(1000) NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def pickup(conn, cur):
    sql = """CREATE TABLE "pickup_1v1" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "host" BOOL NOT NULL  DEFAULT 0,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_2v2" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "host" BOOL NOT NULL  DEFAULT 0,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_3v3" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "host" BOOL NOT NULL  DEFAULT 0,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_4v4" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "host" BOOL NOT NULL  DEFAULT 0,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_5v5" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "host" BOOL NOT NULL  DEFAULT 0,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_game_start" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "team1" VARCHAR NOT NULL ,
        "team2" VARCHAR NOT NULL ,
        "type" VARCHAR NOT NULL ,
        "host" VARCHAR NOT NULL ,
        "map" VARCHAR NOT NULL ,
        "time" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_maps" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "1v1" BOOL NOT NULL ,
        "2v2" BOOL NOT NULL ,
        "3v3" BOOL NOT NULL ,
        "4v4" BOOL NOT NULL ,
        "5v5" BOOL NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    
    ###
    sql = """
        INSERT INTO "pickup_maps" VALUES(1,'East vs West',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(2,'Seaside',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(3,'Marooned 2',1,1,1,0,0);
        INSERT INTO "pickup_maps" VALUES(4,'A Path Beyond',1,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(5,'Caffeinated',1,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(6,'Central Conflict',1,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(7,'Coastal Influence',1,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(8,'High & Low',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(9,'Mjolnir',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(10,'North by NorthWest',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(11,'Pressure',1,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(12,'Raraku',1,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(13,'Regeneration Basin',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(14,'Ring of Fire',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(15,'Keep Off The Grass 2',1,0,0,0,0);
        INSERT INTO "pickup_maps" VALUES(16,'Styrian Mountains',1,0,0,0,0);
        INSERT INTO "pickup_maps" VALUES(17,'Snowy Ridge',1,0,0,0,0);
        INSERT INTO "pickup_maps" VALUES(18,'Bavarian Redux',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(19,'Crossing the River',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(20,'Equal Opportunity',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(21,'First Come, First Served',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(22,'Island Hoppers',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(23,'Middle Mayhem',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(24,'Pearly Wastelands',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(25,'Puddles Redux',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(26,'River War 2',1,1,0,0,0);
        INSERT INTO "pickup_maps" VALUES(27,'Haos Ridges',1,1,1,0,0);
        INSERT INTO "pickup_maps" VALUES(28,'Island Wars III',1,1,1,0,0);
        INSERT INTO "pickup_maps" VALUES(29,'Snowy Island',1,1,1,0,0);
        INSERT INTO "pickup_maps" VALUES(30,'All Connected',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(31,'Center of Attention',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(32,'Ore Isle',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(33,'Alaska Anarchy Redux ',0,1,1,1,1);
        INSERT INTO "pickup_maps" VALUES(34,'Daejeon',0,1,1,1,1);
        INSERT INTO "pickup_maps" VALUES(35,'Fire Alley',0,1,1,1,1);
        INSERT INTO "pickup_maps" VALUES(36,'High & Low Extended',0,0,1,1,1);
        INSERT INTO "pickup_maps" VALUES(37,'Mjolnir 2',0,1,1,1,0);
        INSERT INTO "pickup_maps" VALUES(38,'Doughnut',0,1,1,0,0);
    """
    cur.executescript(sql)
    conn.commit()
    ###
    
    sql = """CREATE TABLE "pickup_stats" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "games" INTEGER NOT NULL  DEFAULT 0,
        "hosts" INTEGER NOT NULL  DEFAULT 0,
        "complaints" INTEGER NOT NULL  DEFAULT 0
        )
    """
    cur.execute(sql)
    conn.commit()

def notify(conn, cur):
    sql = """CREATE TABLE "notify" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        "user" VARCHAR NOT NULL,
        "date" DATETIME NOT NULL,
        "mod" VARCHAR NOT NULL DEFAULT "any",
        "version" VARCHAR NOT NULL DEFAULT "any",
        "timeout" VARCHAR NOT NULL DEFAULT "none",
        "num_players" VARCHAR NOT NULL DEFAULT "no limit",
        "other_options" VARCHAR NOT NULL DEFAULT "NULL" 
        )
    """
    cur.execute(sql)
    conn.commit()

def user_notified(conn,  cur):
    sql = """CREATE TABLE "user_notified" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        "user" VARCHAR NOT NULL,
        "ip" VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def faq(conn, cur):
    sql = """CREATE TABLE "faq" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "item" VARCHAR NOT NULL ,
        "whoset" VARCHAR NOT NULL ,
        "desc" VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def pingme(conn, cur):
    sql = """CREATE TABLE "pingme" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "who" VARCHAR NOT NULL ,
        "users_back" VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def commits(conn, cur):
    sql = """CREATE TABLE "commits" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "title" VARCHAR NOT NULL,
        "repo" VARCHAR NOT NULL,
        "branch" VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def bugs(conn, cur):
    sql = """CREATE TABLE "bugs" (
        "uid" INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL  UNIQUE ,
        "title" VARCHAR NOT NULL,
        "num" VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def activity(conn, cur):
    sql = """CREATE TABLE "activity" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "user" VARCHAR NOT NULL,
        "act" VARCHAR NOT NULL,
        "date_time" date NOT NULL,
        "channel" VARCHAR
        )
    """
    cur.execute(sql)
    conn.commit()

def messages(conn, cur):
    sql = """CREATE TABLE messages (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "user" VARCHAR NOT NULL,
        "message" VARCHAR NOT NULL,
        "date_time" date NOT NULL,
        "channel" VARCHAR NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

def games(conn, cur):
    sql = """CREATE TABLE games (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL,
        "address" VARCHAR NOT NULL,
        "players" VARCHAR NOT NULL,
        "version" VARCHAR NOT NULL,
        "mod" VARCHAR NOT NULL,
        "map" VARCHAR NOT NULL,
        "date_time" date NOT NULL,
        "id" INTEGER NOT NULL DEFAULT 0
        )
    """
    cur.execute(sql)
    conn.commit()
