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

import sqlite3
import os

def start():
    try:
        os.mkdir("db")
        os.chmod("db", 0o700)
    except:
        print("Error! Can not create a directory, check permissions and try again")
        return
    print("Creating databases")
    black_list()
    commands()
    users()
    later()
    pickup()
    notify()
    maps()
    faq()
    pingme()
    commits()
    activity()
    messages()
    games()
    print("Creating databases completed.\tOK")
    
def black_list():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE black_list (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        user varchar(30) NOT NULL,
        date_time date NOT NULL,
        count integer NOT NULL
        )        
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def commands():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE commands (
                uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
                user varchar(30) NOT NULL,
                command varchar(300) NOT NULL,
                date_time date NOT NULL
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
    cur.close()
    
def users():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE users (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        user varchar(30) NOT NULL,
        date date,
        state bool NOT NULL DEFAULT 0,
        channels VARCHAR
        )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def later():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE later (
            uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
            sender varchar(30) NOT NULL,
            reciever varchar(30) NOT NULL,
            channel varchar(30) NOT NULL,
            date date NOT NULL,
            message varchar(1000) NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def pickup():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
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
    cur.close()

def notify():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE "notify" (
        uid INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
        user VARCHAR NOT NULL,
        date DATETIME NOT NULL,
        mod VARCHAR NOT NULL DEFAULT "all",
        version VARCHAR NOT NULL DEFAULT "all",
        timeout VARCHAR NOT NULL DEFAULT "all",
        num_players VARCHAR NOT NULL DEFAULT "all"
    )                
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def maps():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE "maps" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "mod" VARCHAR NOT NULL ,
        "hash" VARCHAR NOT NULL ,
        "title" VARCHAR NOT NULL ,
        "description" VARCHAR,
        "author" VARCHAR,
        "type" VARCHAR NOT NULL ,
        "titleset" VARCHAR NOT NULL ,
        "players" INTEGER NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()
    sql = """
        INSERT INTO "maps" VALUES(1,'ra','2f069fcc457ae941388db3594932c9a93d59615d','A Path Beyond','','Westwood Studios','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(2,'ra','66570c10873e8e42a7defeee13e8ca45367d8a38','Alaska Anarchy Redux','','Buddha','Conquest','SNOW',10);
        INSERT INTO "maps" VALUES(3,'ra','e1b0b14b0eae199b8ad20c60ff00cdc6fa2901cd','All Connected','Great for left vs right or top vs bottom','Buddha','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(4,'ra','606c698f9d4f3a69b7e33daec3d175f76bd74335','Bavarian Redux','2v2; Modification of Bavarian Blast','hamb','Conquest','SNOW',4);
        INSERT INTO "maps" VALUES(5,'ra','6d6f08ba7a9b6e0ce4bedb21ea5ec3affcfa359b','Caffeinated','','C. Forbes & R. Pepperell','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(6,'ra','39d1e0e8a7af677aaa848703466a2c4fa30dbdba','Center of Attention','','Buddha','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(7,'ra','45b808be0a250923d8782c5658b4a0eb741c20f3','Central Conflict','','Westwood Studios','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(8,'ra','73a44013b1be48683f7daddb37262bd540804ffb','Coastal Influence','','Westwood Studios','Conquest','SNOW',8);
        INSERT INTO "maps" VALUES(9,'ra','399372de425c9e8e9d49df90fbbc467dcfc52ac7','Convergence','3 vs 3 Team Map.','Arcturus','Conquest','TEMPERAT',6);
        INSERT INTO "maps" VALUES(10,'ra','8a7c6ad712732e0d7650597c6815c01b505044dd','Crossing the River','','Westwood Studios','Conquest','TEMPERAT',4);
        INSERT INTO "maps" VALUES(11,'ra','2078b95deeff99695f0d135f0083ab484b41a1d0','Daejeon','','Buddha','Conquest','TEMPERAT',10);
        INSERT INTO "maps" VALUES(12,'ra','13c4a52185b537b46acb6a9a62a289f81abc0eab','East vs West','2v2 Teamplay Map','Chris Forbes','Conquest','TEMPERAT',4);
        INSERT INTO "maps" VALUES(13,'ra','deb4c77d00d0cc0eca5339e5a55a8eb8e8cc9fae','Equal Opportunity','','Westwood Studios','Conquest','SNOW',4);
        INSERT INTO "maps" VALUES(14,'ra','aa70920a89df86b6ec4abdbf5f80d1475a7d4086','Fire Alley','4-10','Buddha','Conquest','SNOW',10);
        INSERT INTO "maps" VALUES(15,'ra','9db755ca4dee7b8da372d721f71422cf83c60e95','First Come, First Served','','Westwood Studios','Conquest','TEMPERAT',4);
        INSERT INTO "maps" VALUES(16,'ra','3bc995f925d5b1a894513fb3e570ce22784adcf1','Haos Ridges','Team map','Seru','Conquest','TEMPERAT',6);
        INSERT INTO "maps" VALUES(17,'ra','a1e88759117193b080452a4d27f7e205f476d0c9','High & Low Extended','','Buddha','Conquest','TEMPERAT',10);
        INSERT INTO "maps" VALUES(18,'ra','ba403f6bcb4cae934335b78be42f714992b3a71a','High & Low','','Captain Mel','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(19,'ra','3beaece0b6150f3c742545bba197a9e735aca1ac','Island Hoppers','','Westwood Studios','Conquest','SNOW',4);
        INSERT INTO "maps" VALUES(20,'ra','32e3d46b110da0541991d4f1960dca3ecd6aac35','Island Wars III','','Buddha','Conquest','TEMPERAT',6);
        INSERT INTO "maps" VALUES(21,'ra','a3088b0857f20742b8ebcf78210f2812ae28532e','Keep Off The Grass 2','1v1; Modification of Keep Off The Grass','hamb','Conquest','TEMPERAT',2);
        INSERT INTO "maps" VALUES(22,'ra','931557da9d74550d2a85d3cb92dc37748beda9ff','Crossroads','Classic King of the Hill map for 2-man teams','Chris Forbes','KotH','TEMPERAT',4);
        INSERT INTO "maps" VALUES(23,'ra','5496ebb99b9982b5edaf55b6cc1b1a2dccf5ecc2','Island Hoppers','Island Hoppers, Modified for King of the Hill','Westwood Studios','KotH','SNOW',4);
        INSERT INTO "maps" VALUES(24,'ra','a59eed0405c242bd01ca2d9638561fe1dfbead07','Marooned II','','Westwood Studios','Conquest','TEMPERAT',6);
        INSERT INTO "maps" VALUES(25,'ra','a34f3239845a6d9dae486e6bca97a637ddbd69c2','Middle Mayhem','','Westwood Studios','Conquest','SNOW',4);
        INSERT INTO "maps" VALUES(26,'ra','d19ec877767c2d9075837afd67a1936db43ccd09','Mjolnir','','Westwood Studios','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(27,'ra','735299cd2da69019ebb66d4f689218f5a259c397','North by Northwest','','Westwood Studios','Conquest','SNOW',8);
        INSERT INTO "maps" VALUES(28,'ra','06f3b987c5113f4b11d6ef52494f9221ad662f40','Ore Isle','','Buddha','Conquest','SNOW',8);
        INSERT INTO "maps" VALUES(29,'ra','36f491dbfec74723f0ec6b6f6bc28c4454b8c69b','Pearly Wastelands','','Buddha','Conquest','SNOW',4);
        INSERT INTO "maps" VALUES(30,'ra','fb94aa975815ae780751e251ed438abd17fa162f','Pressure','','Seru','Team Map','TEMPERAT',8);
        INSERT INTO "maps" VALUES(31,'ra','7f13ad84303ac9e9c7cdb178bb32903d13ae712e','Puddles Redux','','Buddha','Conquest','TEMPERAT',4);
        INSERT INTO "maps" VALUES(32,'ra','6889754a5ec6ca5764a43fe4b269dae9f64ddefb','Raraku','','Westwood Studios','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(33,'ra','4c19a69d867fb363a76920b72457f9c78b430ad7','Regeneration Basin','','Westwood Studios','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(34,'ra','af13d472ca2bb0eae60cdbe638a741cbde580e8d','Ring of Fire','','Westwood Studios','Conquest','SNOW',8);
        INSERT INTO "maps" VALUES(35,'ra','3e1e34f90f6c8528e5ffe200ccee30a31a55d50f','River War 2','','Captain Mel','Conquest','TEMPERAT',4);
        INSERT INTO "maps" VALUES(36,'ra','0e8a3d20464962c80253496c262e6017a84d1236','Seaside','2v2 / Free for all','hamb','Conquest','TEMPERAT',4);
        INSERT INTO "maps" VALUES(37,'ra','e3012ad4d176928ecbf9ed7c1f16d5005aefd36c','Snowy Island','','Buddha','Conquest','SNOW',6);
        INSERT INTO "maps" VALUES(38,'ra','938993e56bbe5add578f60d8c2bc6523289b5602','Snowy Ridge','Free-for-all deathmatch in the snow','Chris Forbes','Conquest','SNOW',3);
        INSERT INTO "maps" VALUES(39,'ra','7422387dcbaa64dd250da4907cf944e914b2e8ee','Styrian Mountains','Winter like in Hell','ReFlex','Conquest','SNOW',2);
        INSERT INTO "maps" VALUES(40,'cnc','2b9fed32398d4ee983d8184bd66d0063f4e83970','East vs West 3','3v3 Team Map','Paul Chote','Conquest','WINTER',6);
        INSERT INTO "maps" VALUES(41,'cnc','29cb77c148d188caa412fd594409a960783aa764','Storm the Beachhead','Remake of the first GDI Mission','Westwood Studios','Conquest','TEMPERAT',2);
        INSERT INTO "maps" VALUES(42,'cnc','2b07e1792985b04fd8a0ca9c160984a4ef99f03d','Break of Day','Unbalanced','Petrenko','Conquest','DESERT',4);
        INSERT INTO "maps" VALUES(43,'cnc','0dc2e2c17e1c6ccf2b76bb454d1c1e9d8b16cbec','Chokepoint','A battle over a small stream with only small passes','Tiberian','Conquest','DESERT',2);
        INSERT INTO "maps" VALUES(44,'cnc','91dd8de1a072486d3e76ee326460314f68c1621a','Simple Chord','3V3 with 2 Expansions','Petrenko','Conquest','TEMPERAT',6);
        INSERT INTO "maps" VALUES(45,'cnc','882c1570ea0dc1297153f618e0a183aa9ab2afd1','Dead In Motion','1V1','Petrenko','Conquest','WINTER',2);
        INSERT INTO "maps" VALUES(46,'cnc','01cab429d40f091fe1731bef3e9af36c04fec74d','Tiberium Garden II','Large map for 6p FFA, 2v2v2 or 3v3','Chris Forbes','Conquest','DESERT',6);
        INSERT INTO "maps" VALUES(47,'cnc','0615f12889446ac01a114bb0bb688af1fc01c0af','Instant Karma','Beach to beach - 2V2','Petrenko','Conquest','DESERT',4);
        INSERT INTO "maps" VALUES(48,'cnc','8ac8dcbcd9b3b83fadf67ecd5c9a71e3f91e4093','Into the River Below','"I''m running from the inferno.."','Slendermang','Conquest','WINTER',6);
        INSERT INTO "maps" VALUES(49,'cnc','417afae36eb7e2f52143e72dc2816777d0afd6cb','Llamas','','Chris Forbes','Conquest','WINTER',4);
        INSERT INTO "maps" VALUES(50,'cnc','21e1fcce0edc4730ba9f66a5933e90b53d6bde0e','Llamas 2','2 Players added','Chris Forbes / Petrenko','Conquest','WINTER',6);
        INSERT INTO "maps" VALUES(51,'cnc','366f959c25eb8506b87ff16e4be3ad8b2cd849b5','Minus Two','A teambattle over a small stream with only small passes','Tiberian (Petrenko)','Conquest','DESERT',4);
        INSERT INTO "maps" VALUES(52,'cnc','b76bddd3cbb7c828d1bda040b44216fc8cc46be4','Nullpeter','4v4 Team Map','Paul Chote (Petrenko)','Conquest','WINTER',8);
        INSERT INTO "maps" VALUES(53,'cnc','eba46f0b247ab52e6b9d044b3711a1f28763e634','Crossing the Rubicon','8 Player North vs South Map','Arcturus','Conquest','TEMPERAT',8);
        INSERT INTO "maps" VALUES(54,'cnc','7761208e53d74e2a080255bbe60cf2d2fbc0388c','Sea and Cake','Use sea for air ambushes','Petrenko','Conquest','DESERT',2);
        INSERT INTO "maps" VALUES(55,'cnc','724457304d8a84a14a236d4af6e4c8dec85b575a','The Sentinel','A 1 versus 1 map in an icy place','Tiberian','Conquest','WINTER',2);
        INSERT INTO "maps" VALUES(56,'ra','f9ce9066950638c1b10e9d2d34071a4adacb8071','Doughnut','3v3; Capture oil derricks for extra cash','hamb','Conquest','TEMPERAT',6);
        INSERT INTO "maps" VALUES(57,'ra','0aac7b28eed9e4c09761929f96c7ecd7d919b3a1','Mjolnir 2','4v4','hamb','Conquest','TEMPERAT',8);
    """
    cur.executescript(sql)
    conn.commit()
    cur.close()

def faq():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE "faq" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "item" VARCHAR NOT NULL ,
        "whoset" VARCHAR NOT NULL ,
        "desc" VARCHAR NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def pingme():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE "pingme" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "who" VARCHAR NOT NULL ,
        "users_back" VARCHAR NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def commits():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE "commits" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "title" VARCHAR NOT NULL,
        "repo" VARCHAR NOT NULL,
        "branch" VARCHAR NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()

def activity():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
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
    cur.close()

def messages():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
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
    cur.close()

def games():
    conn = sqlite3.connect('db/openra.sqlite')
    cur = conn.cursor()
    sql = """CREATE TABLE games (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "game" VARCHAR NOT NULL,
        "players" VARCHAR NOT NULL,
        "version" VARCHAR NOT NULL,
        "date_time" date NOT NULL
    )
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
