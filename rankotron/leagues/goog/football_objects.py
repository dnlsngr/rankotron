'''
Created on Nov 9, 2013

@author: dsinger
'''

import re

class WeekStats:
    def __init__(self, player="", points=0):
        self.d_points = points
        self.d_player = player
        
    def print_stats(self):
        return str(self.d_player) + " " + str(self.d_points)
    
    def stream_stats(self):
        return str(self.d_player) + "#" + str(self.d_points)
    
    def reconstitute(self, stream):
        tokens = re.split('\#', stream)
        self.d_player = tokens[0]
        self.d_points = float(tokens[1])
    

class Position:
    def __init__(self, stats, position=""):
        self.d_position = position
        self.d_stats = stats
    
    def stream_pos(self):
        result = self.d_position + "@"
        
        first = True
        for stat in self.d_stats:
            if first:
                first = False
                result = result + str(stat.stream_stats())
            else:
                result = result + "+" + str(stat.stream_stats())
        
        return result
        
    def reconstitute(self, stream):
        pos_name_tokens = re.split("\@", stream)
        self.d_position = pos_name_tokens[0]
        stat_tokens = re.split("\+", pos_name_tokens[1])
        for stat_token in stat_tokens:
            stat = WeekStats()
            stat.reconstitute(stat_token)
            self.d_stats.append(stat)
        
    def print_pos(self):
        result = str(self.d_position) + " stats: <br>"
        count = 1
        for statline in self.d_stats:
            result = result + "___Week " + str(count) + ": " + str(statline.print_stats()) + "<br>"
            count = count + 1
        result = result + "<br>"
        return result
    
class Team:
    def __init__(self, positions, name=""):
        self.d_name = name
        self.d_positions = positions
            
    def get_num_weeks(self):
        if (len(self.d_positions) == 0):
            return 0
        else:
            return len(self.d_positions[0].d_stats)
        
    def stream_team(self):
        result = self.d_name + "|"
        first = True
        for pos in self.d_positions:
            if first:
                first = False
                result = result + str(pos.stream_pos())
            else:
                result = result + "~" + str(pos.stream_pos())
        return result
    
    def reconstitute(self, stream):
        team_name_tokens = re.split("\|", stream)
        self.d_name = team_name_tokens[0]
        position_tokens = re.split("\~", team_name_tokens[1])
        for pos_token in position_tokens:
            pos = Position([])
            pos.reconstitute(pos_token)
            self.d_positions.append(pos)
        return self.get_num_weeks()
        
        
    def team_str(self):
        result = "Team Name: " + str(self.d_name) + '<br><br>'
        for pos in self.d_positions:
            result = result + str(pos.print_pos()) + " <br>"
        return result
            