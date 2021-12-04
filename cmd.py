# Weather Tracker | cmd.py
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
# * 11/27/2021
#   -
#--------------------------------------------------
# Known Issues:
# 1. 
#
#--------------------------------------------------
from inputimeout import inputimeout, TimeoutOccurred
import os

class CmdInterface():
    def __init__(self, scraper, toolbox):
        # self.DisplayMain()
        self.scraper = scraper
        self.toolbox = toolbox
        self.exit = False
        self.live = False
        self.toolbox.ConvertObj(self.scraper.ScrapePage())
        self.DisplayMain()

    def DisplayGraphing(self):
        print('Weather Tracker Graphing Options')
        print('====================================')
        print('Graphing Options')
        print('1. Option 1')
        print('2. Option 2')
        
        while not self.exit:
            sel = input(":")

            if sel == '1':
                pass
            elif sel == '2':
                pass
            elif sel == '-back':
                return
            elif sel == '--quit':
                self.exit = True
            else:
                print()
                print('That is not a recognized command..')
                print()

    def DisplayMain(self):
        print('Weather Tracker')
        print('====================================')
        while not self.exit:
            try:
                if self.live:
                    self.toolbox.PrintFrameData()
                print('Type a command: (--help for help)')

                # Input command will timeout every 30 seconds. At which time, the website will be queried again
                sel = inputimeout(">>", timeout=30)

                if sel == '--help':
                    print()
                    print('-live\tShow data as it is ingressed')
                    print('-graph\tDisplay graphing options')
                    print('-quit or q\tClose the application')
                    print()           

                elif sel == '-live':
                    if self.live:
                        self.live = False
                    else:
                        self.live = True
                    continue


                elif sel == '-graph':
                    self.DisplayGraphing()
                    continue

                elif sel == '--quit':
                    self.exit = True

                else:
                    print()
                    print('That is not a recognized command..')
                    print()

            except TimeoutOccurred:
                self.toolbox.ConvertObj(self.scraper.ScrapePage())

            finally:
                os.system('cls' if os.name == 'nt' else 'clear')
                

            