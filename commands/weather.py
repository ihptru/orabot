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

import pywapi

def weather(self, user, channel):
    def weather_usage():
        message = "(]weather [--current|--forecast|--all] [US zip code | US/Canada city, state | Foreign city, country]) -- Returns the approximate weather conditions for a given city from Google Weather. --current, --forecast, and --all control what kind of information the command shows."
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
        self.irc_sock.send( str_buff.encode() )

    command = (self.command)
    command = command.split()
    if ( len(command) == 1 ):
        weather_usage()
    elif ( len(command) > 1 ):
        if ( command[1] == "--current" ):
            if ( len(command) == 2 ):
                weather_usage();
            else:
                try:
                    location = command[2]
                    data = pywapi.get_weather_from_google(location)
                    city = data.get("forecast_information").get("city")
                    current = data.get("current_conditions")
                    message = "Current weather for "+city+" | Temperature: "+current.get("temp_c")+"°C; "+current.get("humidity")+"; Conditions: "+current.get("condition")+"; "+current.get("wind_condition")
                    self.send_reply( (message), user, channel )
                except:
                    message = "Error: No such location could be found."
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
        elif (command[1] == "--forecast" ):
            if ( len(command) == 2 ):
                weather_usage()
            else:
                try:
                    location = command[2]
                    data = pywapi.get_weather_from_google(location)
                    city = data.get("forecast_information").get("city")
                    length = len(data.get("forecasts"))
                    weathers = []
                    for i in range(int(length)):
                        day_of_week = data.get("forecasts")[i].get("day_of_week")
                        conditions = data.get("forecasts")[i].get("condition")
                        high_temp = str(int(round((int(data.get("forecasts")[i].get("high"))-32)/1.8)))
                        low_temp = str(int(round((int(data.get("forecasts")[i].get("low"))-32)/1.8)))
                        weathers.append(day_of_week+": "+conditions+"; High of "+high_temp+"°C; Low of "+low_temp+"°C")

                    message = "Forecast for " +city+" | "+" | ".join(weathers)
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                except:
                    message = "Error: No such location could be found."
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
        elif (command[1] == "--all" ):
            if ( len(command) == 2 ):
                weather_usage()
            else:
                try:
                    location = command[2]
                    data = pywapi.get_weather_from_google(location)
                    city = data.get("forecast_information").get("city")
                    current = data.get("current_conditions")
                    length = len(data.get("forecasts"))
                    weathers = []
                    weathers.append("Weather for "+city+" | Temperature: "+current.get("temp_c")+"°C; "+current.get("humidity")+"; Conditions: "+current.get("condition")+"; "+current.get("wind_condition"))
                    for i in range(int(length)):
                        day_of_week = data.get("forecasts")[i].get("day_of_week")
                        conditions = data.get("forecasts")[i].get("condition")
                        high_temp = str(int(round((int(data.get("forecasts")[i].get("high"))-32)/1.8)))
                        low_temp = str(int(round((int(data.get("forecasts")[i].get("low"))-32)/1.8)))
                        weathers.append(day_of_week+": "+conditions+"; High of "+high_temp+"°C; Low of "+low_temp+"°C")
                    message = " | ".join(weathers)
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
                except:
                    message = "Error: No such location could be found."
                    str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                    self.irc_sock.send (str_buff.encode())
        else:
            try:
                location = command[1]
                data = pywapi.get_weather_from_google(location)
                city = data.get("forecast_information").get("city")
                current = data.get("current_conditions")
                message = "Current weather for "+city+" | Temperature: "+current.get("temp_c")+"°C; "+current.get("humidity")+"; Conditions: "+current.get("condition")+"; "+current.get("wind_condition")
                self.send_reply( (message), user, channel )
            except:
                message = "Error: No such location could be found."
                str_buff = ( "NOTICE %s :%s\r\n" ) % (user,message)
                self.irc_sock.send (str_buff.encode())
