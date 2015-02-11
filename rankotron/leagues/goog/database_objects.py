'''
Created on Nov 24, 2013

@author: dsinger
'''
from football_objects import Team
from football_objects import Position
from football_objects import WeekStats

from google.appengine.ext import ndb

import re

class LeagueGD(ndb.Model):
    userid = ndb.IntegerProperty(required=True)
    teams = ndb.TextProperty(repeated=True)
        
        
class LeagueStoreGD:
    loadedLeague = ""
    
    def putLeague(self, userid, teamDict):
        print(str(userid))
        teams = []
        for team_id, team in teamDict.iteritems():
            team_str = str(team_id) + "%" + team.stream_team()
            teams.append(team_str)
        stor_obj = LeagueGD(id=userid, userid=userid, teams=teams)
        print(stor_obj.teams)
        stor_obj.put()
        
    def getTeamMapFromDB(self, userid):
        leagueKey = ndb.Key('LeagueGD', userid)
        leagueEntry = leagueKey.get()

        if (leagueEntry == None):
            print("no matches")
            return (None, None)
        else:
            print("found entry")
            print(leagueEntry)
            if (leagueEntry != None):
                team_map = dict()
                for team in leagueEntry.teams:
                    id_tokens = re.split("%", team)
                    team_id = int(id_tokens[0])
                    team = Team([], "")
                    weeks = team.reconstitute(id_tokens[1])
                    team_map[team_id] = team
                
                return (team_map, weeks)
    

        