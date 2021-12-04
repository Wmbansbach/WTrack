import datapoint
import sqlite3
import pandas as pd
from tabulate import tabulate
import os

class StorageTools:
    def __init__(self) -> None:
        self.nday = False
        self.dataframe = pd.DataFrame()
        self.home_dir = os.environ["HOMEPATH"]

        # Check for Program Directory - Create if does not exist
        if not os.path.isdir(os.path.join(self.home_dir, "_WTrack")):
            os.mkdir(os.path.join(self.home_dir, "_WTrack"))

        # Set Database and CSV file paths and names
        self.db_path = os.path.join(self.home_dir, "_WTrack", "WTracker.sqlite")
        self.csv_path = os.path.join(self.home_dir, "_WTrack", "WTracker.csv")

        
        # Open a db connection
        self.db_conn = sqlite3.connect(self.db_path)

    def ConvertObj(self, wdata):
        # Convert list of cleaned data into Datapoint object
        dp = datapoint.DataPoint()
        dp.datetime = wdata[0]
        dp.curr_temp = wdata[1]
        dp.wind = wdata[3]
        dp.wind_gust = wdata[4]
        dp.humidity = wdata[5]
        dp.pressure = wdata[8]
        dp.cloud_cover = wdata[9]
        dp.cloud_height = wdata[11]
        if len(wdata) == 14:
            dp.high = wdata[12]
            dp.low = wdata[13]
            self.nday = True
        self.ConvertFrame(dp)

    def PrintFrameData(self):
        print(tabulate(self.dataframe, headers = "keys"))


    def ConvertFrame(self, datapoint):
        # Take DataPoint object and convert to pandas dataframe
        frame = pd.DataFrame()
        buffer = {"Timestamp": pd.Series([str(datapoint.datetime)]),
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
        self.dataframe = self.dataframe.append(frame)   

        # Create/Append data to sql db, commit changes, create csv file
        frame.to_sql("Weather Datapoints", self.db_conn, if_exists='append')
        self.db_conn.commit()

        # Push entire dataframe to csv
        self.dataframe.to_csv(path_or_buf = self.csv_path, na_rep = "-")

        # Nicely Output Frame Data
        # print("Frame\n" + tabulate(frame, headers = buffer.keys()))

    def CloseDatabase(self):    
        self.db_conn.close()

    
            




