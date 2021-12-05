# Weather Tracker | PullPageData.py
#--------------------------------------------------
# Synopsis: Class handles scraping of webpage , cleans it, and returns data in a list
#           
#--------------------------------------------------
# Documentation:
# * Parameters
#   > [Param 1]   - [Param 1 Description]
#   
# * Example
#   > [Example 1]
#
# * Logging
#   > [Description] 
#
#--------------------------------------------------
# Change Log:
# * 11/25/2021
#   - Initial concept created
#--------------------------------------------------
# Known Issues:
# 1. Location is hard-coded
# 2. init_url must be an accuweather location and use the More Details Page. The Regular page will break the app
#--------------------------------------------------

import bs4 as beaut
import urllib.request as urllib
from datetime import datetime, date
import re
import bs4.builder._lxml

class PullPageData():
    def __init__(self) -> None:
        self.sys_date = any
        self.init_url = "https://www.accuweather.com/en/us/lake-worth/33460/current-weather/332279"
        self.request = any
        self.SetHeaders(self.init_url)      

    def SetHeaders(self, target):
        browser_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        request_header = {"User-Agent": browser_agent}

        self.request = urllib.Request(target, headers= request_header)

    def ScrapePage(self):
        """ Relevant Data:
            > Date & Time Stamp
            > Current Temperature (Degrees Fehrenheit)
            > Wind (MPH)
            > Wind Gusts (MPH)
            > Humidity (%)
            > Pressure (In Mercury?)
            > Cloud Cover (%)
            > Cloud Ceiling (ft)
            > Daily High (Degrees Fehrenheit)
            > Daily Low Temperatures (Degrees Fehrenheit)
        """
        with urllib.urlopen(self.request) as response:
            html = response.read()
            weather_data = list()
            _html = beaut.BeautifulSoup(html, "lxml")

            # Append Date & Time Stamp to list
            weather_data.append(datetime.now().strftime("%A - %B %d %Y - %I:%M:%S%p"))
            # print(_html.find_all())
            # Parse Current Weather Data
            # print(_html.find_all("div", class_= ["detail-item spaced-content", "display-temp"]))
            cw_data_raw = _html.find_all("div", class_= ["detail-item spaced-content", "display-temp"])
            """Raw Data Before Cleaning:
                > Current Temperature
                > UV Index
                > Wind Speed
                > Wind Gust
                > Humidity
                > Indoor Humidity
                > Dew Point
                > Pressure
                > Cloud Cover
                > Visibility
                > Cloud Ceiling
                """
            # Clean html from data and add to list
            for crd in cw_data_raw:
                form_string = crd.text.format()
                s_list = form_string.split("\n")
                weather_data.append(s_list[len(s_list)-2])

            # High and Low for Day (Only Pull Once Daily)
            # print((_html.find_all("div", class_= "temperature", limit=2)))
            if date.today() != self.sys_date:
                hl_data_raw = _html.find_all("div", class_= "temperature", limit=2)
                for drd in hl_data_raw:
                    form_string = drd.text.format()
                    weather_data.append(form_string.strip())
                self.sys_date = date.today()

        # Clean integer data with no extra chars
        wd_clean = [weather_data[0]]
        for val in weather_data[1:]:
            wd_clean.append(re.sub("[^0-9]", "", val))
        
       # print(weather_data)

        return wd_clean
