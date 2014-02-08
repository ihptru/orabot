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

"""
Shows last not commented issues or pull requests from OpenRA bug tracker. Amount as an optional argument.
"""

import urllib.request
import json

def issues(self, user, channel):
	command = (self.command).split()
	if len(command) > 2:
		return
	if len(command) == 2:
		try:
			amount = int(command[1])
		except:
			return
		if amount > 10:
			amount = 10
		use_notice = True
	else:
		amount = 3
		use_notice = False
	url = 'https://api.github.com/repos/OpenRA/OpenRA/issues'
	try:
		data = urllib.request.urlopen(url).read().decode()
		data = json.loads(data)
	except:
		print("*** [%s] Could not fetch a list of OpenRA bugs, apparently 'Exceed Rate Limit'" % self.irc_host)
		return
	result = []
	for report in data:
		if report['comments'] == 0:
			if report['pull_request']['html_url'] == None:
				ttype = "Issue"
			else:
				ttype = "Pull request"
			result.append([report['number'], report['title'], ttype])
		if len(result) == amount:
			break
	for i in range(len(result)):
		if not use_notice:
			self.send_reply( "%s: http://bugs.open-ra.org/%s | %s" % (result[i][2], result[i][0], result[i][1]), user, channel )
		else:
			self.send_notice( "%s: http://bugs.open-ra.org/%s | %s" % (result[i][2], result[i][0], result[i][1]), user)
