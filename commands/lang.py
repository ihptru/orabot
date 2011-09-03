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

languages=['af','sq','ar','be','bg','ca','zh-CN','hr','cs','da','nl','en','et','tl','fi','fr','gl','de','el','iw','hi','hu','is','id','ga','it','ja','ko','lv','lt','mk','ml','mt','no','fa','pl','ro','ru','sr','sk','sl','es','sw','sv','th','tr','uk','vi','cy','yi']
real_langs=['Afrikaans','Albanian','Arabic','Belarusian','Bulgarian','Catalan','Chinese_Simplified','Croatian','Czech','Danish','Dutch','English','Estonian','Filipino','Finnish','French','Galician','German','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Irish','Italian','Japanese','Korean','Latvian','Lithuanian','Macedonian','Malay','Maltese','Norwegian','Persian','Polish','Romanian','Russian','Serbian','Slovak','Slovenian','Spanish','Swahili','Swedish','Thai','Turkish','Ukrainian','Vietnamese','Welsh','Yiddish']

def lang(self, user, channel):
    command = (self.command)
    command = command.split()
    if ( len(command) == 2 ):
        re_str = command[1]
        length = int(len(real_langs))
        lang = []
        code = []
        p = re.compile(re_str, re.IGNORECASE)
        for i in range(length):
            if p.search(real_langs[i]):
                lang.append(real_langs[i])
                code.append(languages[i])
        if ( len(lang) > 1 ):
            self.send_reply( ("Too many matches, be more specific"), user, channel )
        elif ( len(lang) == 0 ):
            self.send_reply( ("No matches"), user, channel )
        else:
            self.send_reply( (code[0] + "      " + lang[0]), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
