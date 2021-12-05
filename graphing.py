import matplotlib.pyplot as plt
import numpy as np



class GraphData:
    def __init__(self, dataframe):
        self.df_val_arry = dataframe.values
        self.df_col_arry = dataframe.columns
        
        pass
        
    def GetOverallChart(self):
        plt.rcdefaults()
        fig, ax = plt.subplots()        
        for i in self.df_col_arry:
            plt.plot(i)
        
        plt.show()
    
    def getTeamData(self):
        teamDict = {}
        checked_list = []
        # Compare team names of each player
        for val in self.p_dict.values():
            if val.team in checked_list:
                teamDict[val.team] += 1     # increment duplicate teams within dict
            else:
                checked_list.append(val.team)   # append non-duplicate to list
                teamDict[val.team] = 1          # create new dict entry

        # Filter teams with more than 1 player in Top 100
        buffer_dict = {}
        for team, amt in teamDict.items():
            if amt > 1:
                buffer_dict[team] = amt
        
        # Breakdown dict into seperate lists
        teams = []
        frequency = []
        for key, val in buffer_dict.items():
            teams.append(key)
            frequency.append(val)

        return tuple(teams), tuple(frequency)
                
    def getGradeChart(self):
        
        labels = 'Freshman', 'Sophmore', 'Junior', 'Senior'
        sizes = self.getGradeData()
        fig1, ax1 = plt.subplots()
        fig1.canvas.set_window_title("Grade Distribution")
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()

    def getGradeData(self):
        total_count = 0 
        freshman = 0
        sophmore = 0
        junior = 0
        senior = 0
        # Parse dict for player grades, tally each respectively
        for val in self.p_dict.values():
            if 'Fr.' in val.grade:
                freshman += 1
            elif 'So.' in val.grade:
                sophmore += 1
            elif 'Jr.' in val.grade:
                junior += 1
            else:
                senior += 1
            total_count += 1

        return [ (freshman / total_count) * 100,
                (sophmore / total_count) * 100,
                (junior / total_count) * 100,
                (senior / total_count) * 100 ]