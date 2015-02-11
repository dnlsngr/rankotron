'''
Created on Nov 16, 2013

@author: dsinger
'''

import urllib2
import re
import sys

from bs4 import BeautifulSoup

# from football_objects import Team
# from football_objects import Position
# from football_objects import WeekStats

from models import League, Team, Week, Position

class URLParser():

    @staticmethod
    def getBaseURL(startingAddress):
        split_url = re.split('\?', startingAddress)
        arg_str = split_url[1]
        args = re.split('&', arg_str)
        final_url_arr = ['http://games.espn.go.com/ffl/boxscorequick?']
        for arg in args:
            if arg.find('leagueId') != -1:
                final_url_arr.append(arg)
                final_url_arr.append('&')
            elif arg.find('seasonId') != -1:
                final_url_arr.append(arg)
                final_url_arr.append('&')
        
        return ''.join(final_url_arr)
    
    
    @staticmethod
    def getWeekLimit(startingAddress):
        website = urllib2.urlopen(startingAddress)
        website_html = URLParser.readURL(startingAddress)
        if (website_html == False):
            print("Error: failed to read site in getWeekLimit")
        matches = re.findall('Record:.*([0-9])\-([0-9]) <', website_html)
        if (matches[0]):
            return int(matches[0][0]) + int(matches[0][1])
        else:
            print ("Error: could not parse week limit from setup page")
            return 0
            
    @staticmethod
    def getUserId(startingAddress):
        exprLeag = 'leagueId=([0-9]*)'
        matchLeag = re.search(exprLeag, startingAddress)
        leag = matchLeag.group(1)
        
        exprTeam = 'teamId=([0-9]*)'
        matchTeam = re.search(exprTeam, startingAddress)
        team = matchTeam.group(1)
        
        return str(leag)# + str(team)
            
    @staticmethod
    def readURL(url):
        try:
            
            website = urllib2.urlopen(url)
            return website.read()
            
        except urllib2.HTTPError, e:
            print "Cannot retrieve URL: HTTP Error /var/wwwde", e.code
            return False
        except urllib2.URLError, e:
            print "Cannot retrieve URL: " + e.reason[1]
            return False

#TODO: make this parsing code more robust, learn about webscraping
class TeamPageParser():
    @staticmethod
    def getAllTeams(teamURL):
        page = URLParser.readURL(teamURL)
        if page == False:
            return False
        
        soup = BeautifulSoup(page)
        matches = soup.find_all('ul', id='games-tabs1')
        if (len(matches) != 1):
            print ("len matches was " + str(len(matches)))
            return False
        
        
        contents = matches[0].contents
        count = 1 # team ids are 1 indexed
        team_map = dict()
        for item in contents:
            team_name = item.a.contents[0]
            team = Team([], team_name)
            team_map[count] = team
            count = count + 1
            
        
        return team_map

#TODO: make this parsing code more robust, learn about webscraping
class MatchupPageParser():
    
    @staticmethod
    def getMatchupTeams(soup):
        matches = soup.find_all('div', style='float:left; border-right:1px solid #dddddd; line-height:0px;')
        if (len(matches) != 2):
            print("Error, did not find team id links. Len was " + str(len(matches)))
            return False
        if matches[0].a == None or matches[1].a == None:
            print("Error, img tags did not have single content")
            
            
        try:
            expr = '(teamId=)([0-9]{1,2})'
            match1 = re.search(expr, matches[0].a['href'])
            team1 = match1.group(2)
            match2 = re.search(expr, matches[1].a['href'])
            team2 = match2.group(2)
            return int(team1), int(team2)
        
        except (KeyError):
            print("Somehow found img link without an href")
            return False
        except (TypeError):
            print("Somehow regex compilation failed")
        except:
            print("Something dastardly occurred in the team parsing")
    
    @staticmethod
    def generatePlayersWithSoup(data_list, team):
        count = 0
        for entry in data_list:
            if entry['class'][0] == 'pncPlayerRow':
                for cell in entry.contents:
                    if (cell.has_key('class')):
                        tokens = cell['class']
                        for class_token in tokens:
                            if (class_token == 'playerSlot'):
                                position = cell.string
                            elif (class_token == 'playertablePlayerName'):
                                name = cell.a.contents[0]
                            elif (class_token == 'appliedPoints'):
                                points = cell.string
                                if points == '--':
                                    points = 0
                                
                new_weekStats = WeekStats(name, points)
                if (len(team.d_positions) > count):
                    team.d_positions[count].d_stats.append(new_weekStats)
                else:
                    new_position = Position([new_weekStats], position)
                    team.d_positions.append(new_position)
                
                count = count + 1
    
    @staticmethod
    def parsePageWithSoup(weekURL, team_map):
        page = URLParser.readURL(weekURL)
        print(weekURL)
        if page == False:
            return False
        
        soup = BeautifulSoup(page)
        (team1, team2) = MatchupPageParser.getMatchupTeams(soup)
        
        table_matches = soup.find_all('table', { 'class' : 'playerTableTable tableBody'})
        MatchupPageParser.generatePlayersWithSoup(table_matches[0], team_map[team1])
        MatchupPageParser.generatePlayersWithSoup(table_matches[1], team_map[team2])
        
        return True
        
