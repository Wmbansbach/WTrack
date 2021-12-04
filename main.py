# Weather Tracker | main.py
#--------------------------------------------------
# Synopsis: Track local weather patterns using data scraped from AccuWeather.com
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
# * 12/4/2021
#   - Completed Initial concept
#   - Got the thing to work
#--------------------------------------------------
# Known Issues:
# 1. 
#
#--------------------------------------------------

from ppd import PullPageData
from storage_tools import StorageTools
from cmd import CmdInterface


stor_tools = StorageTools()
ppd = PullPageData()

interface = CmdInterface(ppd, stor_tools)

stor_tools.CloseDatabase()