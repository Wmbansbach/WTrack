# Weather Tracker | graphing.py
#--------------------------------------------------
# Synopsis: Class contains all methods and attributes to build graphs from stored data
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
# * 12/4/2021
#   - Initial Creation
#--------------------------------------------------
# Known Issues:
# 1. 
#--------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np


class GraphData:
    def __init__(self):
        pass
        
    def TemperatureTSeries(self, dataframe):
        time_df = dataframe['Time']
        temp_df = dataframe['Current_Temperature']
        buffer = []
        
        for i in time_df:
            date, time = i.split('-')
            buffer.append(time)
        time_df = buffer

        plt.rcdefaults()
        plt.plot(time_df, temp_df)

        plt.title('Temperature Over Time')
        plt.xlabel('Time')
        plt.ylabel('Temperature (Degrees F)')
        plt.xticks(rotation=45)
        plt.show()
    
    