# Copyright 2011-2016 orabot Developers
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
Initialize voting for a specific topic; show results
"""

def voting(self, user, channel):
    command = (self.command).split()
    if ( len(command) >= 2 ):
        conn, cur = self.db_data()
        request = command[1]

        if request == "results":
            if len(command ) == 3:
                request_id = command[2]
                sql = """SELECT uid,topic,active,positive,negative,initialized_by,date_activated FROM voting WHERE uid = %s""" % request_id
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if len(records) == 1:
                    if records[0][2]:
                        active = "active"
                    else:
                        active = "ended"
                    self.send_reply("Voting (%s) by %s from %s, ID(%s): %s | positive: %s, negative: %s" % (active, records[0][5], records[0][6], records[0][0], records[0][1], records[0][3], records[0][4]), user, channel)
                    return
                else:
                    self.send_reply("Nothing found", user, channel)
        elif request == "end":
            if len(command) == 3:
                request_id = command[2]
                sql = """SELECT uid,topic,active,positive,negative FROM voting WHERE uid = %s""" % request_id
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                if len(records) == 1:
                    if not records[0][2]:
                        self.send_reply("Voting is already closed: %s" % records[0][1], user, channel)
                        return
                    sql = """UPDATE voting SET active = 0 WHERE uid = %s""" % request_id
                    cur.execute(sql)
                    conn.commit()
                    self.send_reply("Voting closed: %s | positive: %s, negative: %s" % (records[0][1], records[0][3], records[0][4]), user, channel)
                    return
                else:
                    self.send_reply("Nothing found", user, channel)
        elif request == "+1" or request == "-1":
            action = request[0]
            sql = """SELECT uid,active,positive,negative,users_voted FROM voting WHERE active == 1"""
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if len(records) == 1:
                users_voted = records[0][4].split(',')
                if user in users_voted:
                    self.send_reply("You've already voted", user, channel)
                    return
                users_voted.append(user)
                users_voted = ",".join(users_voted)
                positive = int(records[0][2])
                negative = int(records[0][3])
                if action == "+":
                    positive += 1
                elif action == "-":
                    negative +=1
                sql = """UPDATE voting SET positive = %s, negative = %s, users_voted = '%s' WHERE uid = %s""" % (positive, negative, users_voted, records[0][0])
                cur.execute(sql)
                conn.commit()
                self.send_reply("updated, +: %s / -: %s" % (positive, negative), user, channel)
                return
            else:
                self.send_reply("There are no active votings!", user, channel)
        else:
            topic = " ".join(command[1:])
            sql = """SELECT uid FROM voting WHERE active = 1"""
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if len(records) == 1:
                self.send_reply("There is a voting with ID:%s in progress, end it first." % records[0][0], user, channel)
            elif len(records) == 0:
                sql = """INSERT INTO voting (topic, active, positive, negative, initialized_by, date_activated, users_voted) VALUES ('%s',1,0,0,'%s',date('now'),'')""" % (topic, user)
                cur.execute(sql)
                conn.commit()
                sql = """SELECT uid FROM voting WHERE active = 1"""
                cur.execute(sql)
                records = cur.fetchall()
                conn.commit()
                self.send_reply("Initialized, ID: %s. Use %svoting +/-1 to vote" % (records[0][0], self.command_prefix), user, channel)
                return

