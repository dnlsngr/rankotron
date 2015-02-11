'''
Created on Nov 9, 2013

@author: dsinger
'''

from football_objects import Team

DECIMAL_PLACES = 2
def round_to_places(num):
	displacement_factor = 10 ** DECIMAL_PLACES
	return round(num * displacement_factor) / displacement_factor

class AnalyticsProcessor:
	
	@staticmethod
	def rankTeamsByTotalPoints(team_map, team_analytics):
		totals_map = {}
		for team in team_map.itervalues():
			totalPoints = 0
			for position in team.d_positions:
				for stat in position.d_stats:
					totalPoints = totalPoints + float(stat.d_points)
			
			totals_map[team.d_name] = str(totalPoints)
			
		for team in team_analytics:
			team["totalPoints"] = totals_map[team["name"]]
		
		team_analytics.sort(key=lambda x: x['totalPoints'], reverse=True)
	
	@staticmethod
	def getNumWeeks(team_map):
		teams = team_map.values()
		if len(teams) != 0:
			team = teams[0] # get an arbitrary team
			if len(team.d_positions) == 0:
				print("Failure: no positions in team")
				return 0
			else:
				return len(team.d_positions[0].d_stats)
		else:
			print("Failure: no teams in team map")
			return 0
		
	@staticmethod
	def getAllWeeklyTotalsForTeam(team, numWeeks):
		weekPoints = [0]*numWeeks #initalize each week total to 0
		
		for position in team.d_positions:
			
			count = 0
			for stat in position.d_stats:
				weekPoints[count] = weekPoints[count] + float(stat.d_points)
				count = count + 1
				
		return weekPoints
	
	@staticmethod
	def getWeeklyTotalsForAllTeams(team_map, numWeeks):
		#This restructures the data by week rather than by team/position
		teamWeeklyPoints = [[] for w in range(0, numWeeks)]
		
		count = 0
		for team in team_map.itervalues():
			weekPoints = AnalyticsProcessor.getAllWeeklyTotalsForTeam(team, numWeeks)
			
			#TODO: get number of iterations without accumulator?
			count = 0
			for weeklyTotal in weekPoints:
				teamWeeklyPoints[count].append((team.d_name, weeklyTotal))
				count = count + 1
				
		return teamWeeklyPoints
				
	@staticmethod
	def rankTeamsByHeadToHead (team_map, team_analytics):
		numWeeks = AnalyticsProcessor.getNumWeeks(team_map)
		print ("numWeeks " + str(numWeeks))
		if (numWeeks == 0):
			return
		
		teamWeeklyPoints = AnalyticsProcessor.getWeeklyTotalsForAllTeams(team_map, numWeeks)
		
		team_total_wins_map = {}
		
		for week in teamWeeklyPoints:
			weekmin = min(week, key=lambda x: x[1])[1]
			weekmax = max(week, key=lambda x: x[1])[1]
			norm_factor = weekmax - weekmin
			if (norm_factor <= 0):
				print("Error: weekly min is greater than max")
				return
			
			for teamPoints in week:#of the form (name, weeklyTotal)
				teamName = teamPoints[0]
				wins = (teamPoints[1] - weekmin)/norm_factor
				if team_total_wins_map.has_key(teamName):
					team_total_wins_map[teamName] += wins
				else:
					team_total_wins_map[teamName] = wins
	
		for team in team_analytics:
			exWins = team_total_wins_map[team["name"]]
			team["exH2HWins"] = str(round_to_places(exWins))
		
		team_analytics.sort(key=lambda x: x['exH2HWins'], reverse=True)
	