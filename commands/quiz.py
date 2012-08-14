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

"""
Quiz about OpenRA (quiz q, quiz a, quiz skip, quiz info, quiz scores)
"""

def quiz(self, user, channel):
    command = (self.command).split()
    conn, cur = self.db_data()
    if len(command) == 1:
        self.send_notice("Quiz about OpenRA (quiz q, quiz a, quiz skip, quiz info, quiz scores)", user)
    elif len(command) >= 3:
        if command[1] == "a" or command[1] == "answer":
            answer = " ".join(command[2:])
            sql = """SELECT uid,answer FROM quiz WHERE is_answered = 0
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if len(records) == 0:
                self.send_reply("No quiz going on.", user, channel)
            else:
                if answer.lower() == records[0][1].lower():
                    sql = """UPDATE quiz SET is_answered = 1 WHERE uid = """+str(records[0][0])
                    cur.execute(sql)
                    conn.commit()
                    sql = """SELECT uid,user,points FROM quiz_users WHERE user = '"""+user+"""'
                    """
                    cur.execute(sql)
                    rec = cur.fetchall()
                    conn.commit()
                    if len(rec) == 0:
                        sql = """INSERT INTO quiz_users (user,points) VALUES ('"""+user+"""',2)
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:
                        points = str(int(rec[0][2])+2)
                        sql = """UPDATE quiz_users SET points = """+points+""" WHERE user = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                    self.send_reply("That's correct! "+user+" gets 2 point!", user, channel)
                else:
                    sql = """SELECT uid,user,points FROM quiz_users WHERE user = '"""+user+"""'
                    """
                    cur.execute(sql)
                    rec = cur.fetchall()
                    conn.commit()
                    if len(rec) == 0:
                        sql = """INSERT INTO quiz_users (user,points) VALUES ('"""+user+"""',-1)
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:
                        points = str(int(rec[0][2])-1)
                        sql = """UPDATE quiz_users SET points = """+points+""" WHERE user = '"""+user+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                    self.send_reply("Nope, that's wrong. "+user+" loses -1 point.", user, channel)
    elif len(command) == 2:
        if command[1] == "q" or command[1] == "question":
            sql = """SELECT uid,question FROM quiz WHERE is_answered = 0
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if len(records) == 0:
                sql = """SELECT uid,question FROM quiz ORDER BY RANDOM() LIMIT 1
                """
                cur.execute(sql)
                rec = cur.fetchall()
                conn.commit()
                sql = """UPDATE quiz SET is_answered = 0 WHERE uid = """+str(rec[0][0])
                cur.execute(sql)
                conn.commit()
                self.send_reply("Q #"+str(rec[0][0])+": "+rec[0][1], user, channel)
            else:
                self.send_reply("Q #"+str(records[0][0])+": "+records[0][1], user, channel)
        if command[1] == "a" or command[1] == "answer":
            self.send_reply("(quiz a|answer <guess>) -- Let's you answer the question. Checks if <guess> matches the right answer and adjusts user score accordingly.", user, channel)
        if command[1] == "skip":
            sql = """SELECT uid FROM quiz WHERE is_answered = 0
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if len(records) == 0:
                self.send_notice("There is nothing to skip!", user)
            else:
                sql = """UPDATE quiz SET is_answered = 1 WHERE is_answered = 0"""
                cur.execute(sql)
                conn.commit()
                sql = """SELECT uid,user,points FROM quiz_users WHERE user = '"""+user+"""'
                """
                cur.execute(sql)
                rec = cur.fetchall()
                conn.commit()
                if len(rec) == 0:
                    sql = """INSERT INTO quiz_users (user,points) VALUES ('"""+user+"""',-2)
                    """
                    cur.execute(sql)
                    conn.commit()
                else:
                    points = str(int(rec[0][2])-2)
                    sql = """UPDATE quiz_users SET points = """+points+""" WHERE user = '"""+user+"""'
                    """
                    cur.execute(sql)
                    conn.commit()
                self.send_reply(user+" skipped the question and lost -2 points.", user, channel)
        if command[1] == "scores":
            sql = """SELECT user,points FROM quiz_users ORDER BY points LIMIT 10"""
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            result = ""
            for i in range(len(records)):
                result = result + "["+str(i+1)+"] "+records[i][0]+": "+str(records[i][1])+" "
            if len(records) != 0:
                self.send_reply(result, user, channel)
        if command[1] == "info":
            uid = ""
            sql = """SELECT uid FROM quiz WHERE is_answered = 0
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if len(records) != 0:
                uid = str(records[0][0])
            if uid != "":
                uid =  " Current question ID is "+uid+"."
            sql = """SELECT uid FROM quiz"""
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            self.send_reply("There are "+str(len(records))+" questions in the database."+uid, user, channel)
