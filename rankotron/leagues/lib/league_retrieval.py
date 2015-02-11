'''
Created on Dec 7, 2013

@author: dsinger
'''

from parsers import MatchupPageParser
from parsers import TeamPageParser
from parsers import URLParser


#from football_objects import Team
#from database_objects import LeagueStoreGD

def parseWeekRange(startingAddress, start, end, team_map):

    baseURL = URLParser.getBaseURL(startingAddress)

    for week in range(start, (end + 1)):
        print ("week is " + str(week))
        weekURL = baseURL + '&scoringPeriodId=' + str(week)
        
        for team_id, team in team_map.iteritems():
            if team.get_num_weeks() < week:
                print("Parsing team " + str(team.d_name))
                teamWeekURL = weekURL + "&teamId=" + str(team_id)
                MatchupPageParser.parsePageWithSoup(teamWeekURL, team_map)
            else:
                print("Already parsed " +  str(team.d_name) + " this week")
       

def getLeague(startingAddress):
    user_id = int(URLParser.getUserId(startingAddress))
    limit = URLParser.getWeekLimit(startingAddress)
    
    #dbManager = LeagueStoreGD()
    #(team_map, weeks) = dbManager.getTeamMapFromDB(user_id)
    # if (team_map != None):
    #     print("Found a league with weeks: " + str(weeks))
    #     if (weeks < limit):
    #         print(str(weeks) + " is less than the limit of " + str(limit))
    #         parseWeekRange(startingAddress, (weeks+1), limit, team_map)
    #         dbManager.putLeague(user_id, team_map)
    # else:
    print("Not here??") 
    league = 
    team_map = TeamPageParser.getAllTeams(startingAddress)
    parseWeekRange(startingAddress, 1, limit, team_map)
    #dbManager.putLeague(user_id, team_map)
    
    return team_map