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

def start(self):
    conn, cur = self.db_data()
    print(("[%s] Creating database") % (self.irc_host))
    
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
    quiz(conn, cur)

    cur.close()
    print(("[%s] Creating database completed.\tOK") % (self.irc_host))
    
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
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_2v2" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_3v3" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_4v4" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_5v5" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "timeout" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_6v6" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
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
        "map" VARCHAR NOT NULL ,
        "maphash" VARCHAR NOT NULL,
        "time" DATETIME NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    sql = """CREATE TABLE "pickup_maps" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "hash" VARCHAR NOT NULL ,
        "1v1" BOOL NOT NULL ,
        "2v2" BOOL NOT NULL ,
        "3v3" BOOL NOT NULL ,
        "4v4" BOOL NOT NULL ,
        "5v5" BOOL NOT NULL ,
        "6v6" BOOL NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

    sql = """
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Keep Off The Grass 2','a3088b0857f20742b8ebcf78210f2812ae28532e',1,0,0,0,0,0);
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Man to Man','11fd2f8a4a8b54d62ed076287c183c46fe9b2b44',1,0,0,0,0,0);
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Styrian Mountains','5d357387bb7463c59cf9a6eaf8cba455f6e8ed34',1,0,0,0,0,0);
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Artic Triangle Affair','e2725037c92830933641e98d43625f2a8d576210',1,0,0,0,0,0);
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Baywatch','2a60ed2929aef1f75478aba0b9386006ac0e596c',1,0,0,0,0,0);
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Snowy Ridge','938993e56bbe5add578f60d8c2bc6523289b5602',1,0,0,0,0,0);
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Winter Warzone','b5f87f7efb964e57614d22422ff442645357eb2c',1,0,0,0,0,0);
        INSERT INTO pickup_maps (name,hash,"1v1","2v2","3v3","4v4","5v5","6v6") VALUES ('Ares','0233a8939d91b2370e878167ef65844add8388ae',1,1,0,0,0,0);
    """
    cur.executescript(sql)
    conn.commit()

    sql = """CREATE TABLE "pickup_stats" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "name" VARCHAR NOT NULL ,
        "games" INTEGER NOT NULL  DEFAULT 0,
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

def quiz(conn, cur):
    sql = """CREATE TABLE quiz (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "question" VARCHAR NOT NULL,
        "answer" VARCHAR NOT NULL,
        "is_answered" INTEGER NOT NULL DEFAULT 1
        )
    """
    cur.execute(sql)
    conn.commit()
    
    sql = """CREATE TABLE quiz_users (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "user" VARCHAR NOT NULL,
        "points" INTEGER NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()
    
    sql = """
        INSERT INTO quiz (question,answer) VALUES ('When was OpenRA project started?','2007');
        INSERT INTO quiz (question,answer) VALUES ('What\'s Tanya\'s last name?','Adams');
        INSERT INTO quiz (question,answer) VALUES ('OpenRA was written in?','C#');
    """
    cur.executescript(sql)
    conn.commit()
