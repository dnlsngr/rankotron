'''
Created on Nov 9, 2013

@author: dsinger
'''

import webapp2
import jinja2
import os

from football_objects import Team

import league_retrieval
from analytics import AnalyticsProcessor

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
setuppage = jinja_environment.get_template('setup_page.html')
outputpage = jinja_environment.get_template("output.html")



class SetupPageHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write(setuppage.render())
        
    def post(self):
        startingAddress = self.request.get('startingAddress')
        
        team_map = league_retrieval.getLeague(startingAddress)
        
        result = "<br>" 
        
        team_analytics = [{'name' : team.d_name} for team in team_map.itervalues()]
        AnalyticsProcessor.rankTeamsByTotalPoints(team_map, team_analytics)
        AnalyticsProcessor.rankTeamsByHeadToHead(team_map, team_analytics)
        #return
        print(team_analytics)
        
        result = result +  '<br>Full Breakdown<br><br>'
        for team in team_map.itervalues():
            result = result + team.team_str()
        self.response.out.write(outputpage.render(outputBlock=result, teams=team_analytics))
        
        return