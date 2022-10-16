# Weather Tracker | storage_tools.py
#--------------------------------------------------
# Synopsis: Class contains all methods and attributes to manipulate data
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
# * 11/16/2021
#   - Initial Creation
#--------------------------------------------------
# Known Issues:
# 1. If database is created without High / Low data, sqlite3.OperationalError: table "" has no column named ""
# 1a. Issue is also seen with using read_csv
#--------------------------------------------------
import datapoint
import sqlite3
import pandas as pd
from tabulate import tabulate
import os
from datetime import datetime
from pathlib import Path
from time import sleep

class StorageTools:
    def __init__(self) -> None:
        # Define Formatting, Local Environment, and Storage Variables
        self.nday = False
        self.on_pi = False

        self.sensor = any
        self.live_df = pd.DataFrame()
        self.pi_df = pd.DataFrame()
        
        # Check whether running on Linix or Windows and initialize accordingly
        # Set home directory
        self.home_key = "HOMEPATH"
        if os.name != 'nt':
            self.home_key = "HOME"
            self.on_pi = True

            import pi_data
            try:
                self.sensor = pi_data.SHSensor()
                self.sensor.HatInitialize()
            except OSError:
                print("No Hat Found")
            finally:
                self.sensor = pi_data.HDTSensor()
                
        self.home_dir = os.environ[self.home_key]

        # Check for application Directory - Create if does not exist
        if not os.path.isdir(os.path.join(self.home_dir, "_WTrack")):
            os.mkdir(os.path.join(self.home_dir, "_WTrack"))

        # Set Database and CSV file paths and names
        self.db_path = os.path.join(self.home_dir, "_WTrack", "WTracker.sqlite")
        self.csv_path = os.path.join(self.home_dir, "_WTrack", "WTracker.csv")
        self.pidata_path = os.path.join(self.home_dir, "_WTrack", "WTracker_Pi.csv")

        # Open db connection
        self.db_conn = sqlite3.connect(self.db_path)
    
    def PullPrintCSVData(self, to_print = False):
        # Function called when --show is used
        # Nicely prints csv dataframe data
        df = pd.read_csv(self.csv_path, index_col=[0])
        # Read CSV to Dataframe
        if to_print:
            print('\nSTORAGE VIEW', end='\n------------\n')
            print(tabulate(df, headers = "keys"))
        return df
    
    def PrintFrameData(self):
        # Function called when --live is used
        # Nicely prints live dataframe data
        print('LIVE VIEW', end='\n------------\n')
        print(tabulate(self.live_df.tail(15), headers = "keys"))
        if self.on_pi:
            print('\nPI SENSOR VIEW', end='\n------------\n')
            print(tabulate(self.pi_df.tail(15), headers = "keys"))
    
    def CloseDatabase(self):    
        self.db_conn.close()

    def ConvertObj(self, wdata):
        dp = datapoint.DataPoint()
        try:
            dp.datetime, dp.curr_temp, \
            dp.wind, dp.wind_gust, \
            dp.humidity, dp.pressure, \
            dp.cloud_cover, dp.cloud_height = [wdata[v] for v in (0, 1, 2, 3, 4, 7, 8, 10)]
        
            if len(wdata) == 13:         # To fix case where day and night data scaped changes by one
                dp.high = wdata[11]
                dp.low = wdata[12]
                self.nday = True
            elif len(wdata) == 14:
                dp.high = wdata[12]
                dp.low = wdata[13]
            else:
                # Case where incomplete data is scaped from page
                pass
        except IndexError:
            print(wdata)
            input("INGRESS FAILED: SAVE DATA ABOVE")
        
        self.ProcessAWeatherData(dp)

    def ProcessAWeatherData(self, datapoint):
        # Take DataPoint object and convert to pandas dataframe
        frame = pd.DataFrame()
        # frame.rename_axis("Index")
        buffer = {"Time": pd.Series([str(datapoint.datetime)]),
                       "Current_Temperature": pd.Series([datapoint.curr_temp]),
                       "Wind_Speed": pd.Series([datapoint.wind]),
                       "Wind_Gust": pd.Series([datapoint.wind_gust]),
                       "Humidity": pd.Series([datapoint.humidity]),
                       "Pressure": pd.Series([datapoint.pressure]),
                       "Cloud_Cover": pd.Series([datapoint.cloud_cover]),
                       "Cloud_Height": pd.Series([datapoint.cloud_height])
                    }
        if self.nday:
            buffer.update({"Daily_High": pd.Series([datapoint.high]),
                       "Daily_Low": pd.Series([datapoint.low])})
                      
        frame = frame.append(pd.DataFrame(buffer))

        # Append current interation's data to master dataframe
        self.live_df = self.live_df.append(frame)   

        # Create/Append data to sql db, commit changes
        frame.to_sql("AccuWeather Datapoints", self.db_conn, if_exists='append')
        self.db_conn.commit()

        # Create/Append data to csv file
        file_path = Path(self.csv_path)
        file_exists = file_path.exists()
        try:
            frame.to_csv(file_path, header=not file_exists, mode='a' if file_exists else 'w')
        except PermissionError:
            print()
            print('.CSV file is open... No data will be stored until file is closed...')
            print()
            sleep(2)
        # hdr = False  if os.path.isfile(self.csv_path) else True
        # self.live_df.to_csv(path_or_buf = self.csv_path, na_rep = "N/A", mode='a', header=hdr)
    
    def ProcessPiData(self, tempd, humdd, presd):
        frame = pd.DataFrame()
        buffer = {"Timestamp": pd.Series([datetime.now().strftime("%m/%d/%Y-%I:%M:%S%p")]),
                       "Local_Temperature": pd.Series([tempd]),
                       "Local_Humidity": pd.Series([humdd]),
                       "Local_Pressure": pd.Series([presd])
                    }
        frame = frame.append(pd.DataFrame(buffer))

        # Append current interation's pi sensor data to master dataframe
        self.pi_df = self.pi_df.append(frame)   

        # Create/Append data to sql db, commit changes, create csv file
        frame.to_sql("SenseHat Datapoints", self.db_conn, if_exists='append')
        self.db_conn.commit()

        # Push entire dataframe to csv
        # frame.to_csv(path_or_buf = self.pidata_path, na_rep = "-")
        file_path = Path(self.pidata_path)
        file_exists = file_path.exists()
        try:
            frame.to_csv(file_path, header=not file_exists, mode='a' if file_exists else 'w')
        except PermissionError:
            print()
            print('.CSV file is open... No data will be stored until file is closed...')
            print()
            sleep(2)

    
    
            




