# Copyright 2011-2014 orabot Developers
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
    print(("*** [%s] Creating database") % (self.irc_host))

    users(conn, cur)
    user_channel(conn, cur)
    later(conn, cur)
    pingme(conn, cur)
    activity(conn, cur)

    cur.close()
    print(("*** [%s] Creating database completed") % (self.irc_host))
    
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

def pingme(conn, cur):
    sql = """CREATE TABLE "pingme" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "who" VARCHAR NOT NULL ,
        "users_back" VARCHAR NOT NULL
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

def voting(conn, cur):
    sql = """CREATE TABLE "voting" (
        "uid" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,
        "topic" VARCHAR NOT NULL,
        "active" bool NOT NULL DEFAULT 0,
        "positive" INTEGER DEFAULT 0,
        "negative" INTEGER DEFAULT 0,
        "date_activated" DATE
        )
    """
    cur.execute(sql)
    conn.commit()
