# Weather Tracker | cmd.py
#--------------------------------------------------
# Synopsis: Track local weather patterns using data scraped from AccuWeather.com
#           
#--------------------------------------------------
# Documentation:
# * Parameters
#   > scraper - PullPageData object for scraping page
#   
#   > toolbox - StorageTools object for db, csv processing
#
#--------------------------------------------------
# Change Log:
# * 11/25/2021
#   - Initial concept created
# * 12/19/2021
#   - Changed quit to term
#   - Changed command naming scheme to - instead of --
#   - Added some time for help message to be read before clearing screen
#   - Added commenting
#--------------------------------------------------
# Known Issues:
# 1. Graphing does not work on debian
#--------------------------------------------------
from inputimeout import inputimeout, TimeoutOccurred
import os
from time import sleep
import graphing

class CmdInterface:
    def __init__(self, scraper, toolbox):
        self.scraper = scraper
        self.toolbox = toolbox
        self.grapher = graphing.GraphData() 
        self.exit = False                                   # Flag to end loop when needed
        self.live = False                                   # Switch live view on and off
        self.show = False                                   # Switch show view on and off
        self.toolbox.ConvertObj(self.scraper.ScrapePage())  # Start scraping
        self.DisplayMain()                                  # Initialize txt interface

    def DisplayGraphing(self):                              # Graphing Interface Options
        print('Graphing Options')
        print('====================================')
        print('1. Option 1')
        print('2. Option 2')
        
        while not self.exit:
            sel = input(":")

            if sel == '1':
                self.grapher.TemperatureTSeries(self.toolbox.PullPrintCSVData())
                return
            elif sel == '2':
                pass
            elif sel == '-back':
                return
            elif sel == '-term':
                self.exit = True
            else:
                print()
                print('That is not a recognized command..')
                print()
                sleep(1)
            
    def DisplayMain(self):                                          # Main Interface
        while not self.exit:
            try:                                                    # Check for live and show flags before prompting. 
                if self.live:
                    self.toolbox.PrintFrameData()
                if self.show:
                    self.toolbox.PullPrintCSVData(to_print = True)
                print('\nWeather Tracker')
                print('====================================')
                print('Type a command: (-help for help)')
                sel = inputimeout(">>", timeout=15)                 # Input command will timeout every 30 seconds

                if sel == '-help':                                  # Help Interface Options
                    print('Attack Options')
                    print('====================================')
                    print('-s\tShow all data in Storage file')
                    print('-l\tShow incoming data')
                    print('-g\tDisplay graphing options')
                    print('-q\tClose the application')
                    print()           
                    sleep(3)
                elif sel == '-live' or sel == '-l':                 # Live View
                    if self.live:
                        self.live = False
                    else:
                        self.live = True

                elif sel == '-show' or sel == '-s':                 # Show View
                    if self.show:
                        self.show = False
                    else:
                        self.show = True

                elif sel == '-graph' or sel == '-g':                # Graphing Interface Options
                    self.DisplayGraphing()

                elif sel == '-term' or sel == '-q':                 # End cmd loop to terminate program
                    self.exit = True

                else:
                    print()
                    print('That is not a recognized command..')
                    print()
                    sleep(1)

            except TimeoutOccurred:                                 # Catch inputtimeout 
                self.toolbox.ConvertObj(self.scraper.ScrapePage())  # Scrape page again
                if self.toolbox.on_pi:                              # Pull and Process Pi data if applicable
                    x, y, z = self.toolbox.sensor.GetLocalEnvData()
                    self.toolbox.ProcessPiData(x, y, z)

            finally:
                os.system('cls' if os.name == 'nt' else 'clear')    # Clear screen depending on os

            
