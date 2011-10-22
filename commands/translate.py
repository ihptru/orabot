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

"""
Translate text using Google API.
"""

import urllib.request
import urllib.parse
import config

def translate(self, user, channel):
    command = (self.command).split()
    lang = ['af','sq','ar','be','bg','ca','zh-CN','hr','cs','da','nl','en','et','tl','fi','fr','gl','de','el','iw','hi','hu','is','id','ga','it','ja','ko','lv','lt','mk','ml','mt','no','fa','pl','ro','ru','sr','sk','sl','es','sw','sv','th','tr','uk','vi','cy','yi']
    if ( len(command) < 4 ):
        usage = "Usage: "+config.command_prefix+"translate <from language> <to language> <text to translate>   |   To find out country code, use: "+config.command_prefix+"lang <pattern>    Where <pattern> is a part of country name | For example, to translate from English to German: "+config.command_prefix+"translate en de Thank you"
        self.send_notice(usage, user)
        return
    if command[1].lower() in lang:
        from_l = command[1]
    else:
        self.send_reply( ("No such language: " + command[1]), user, channel)
        return
    if command[2].lower() in lang:
        to_l = command[2].lower()
    else:
        self.send_reply( ("No such language: " + command[2]), user, channel)
        return
    params = urllib.parse.urlencode({'v': "1.0", 'q': " ".join(command[3:]), 'langpair': from_l + "|" + to_l})
    f = urllib.request.urlopen("http://ajax.googleapis.com/ajax/services/language/translate?%s" % params)
    a = f.read().decode()
    a = a[a.find("translatedText") +17:]
    t_text = a[:a.find("\"")]
    self.send_reply( (t_text), user, channel)
