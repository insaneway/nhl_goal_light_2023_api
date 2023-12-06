import requests
import datetime
from dateutil import tz
import pause
import json

NHL_API_URL = "https://api-web.nhle.com/v1/"


def get_teams():
    """ Function to get a list of all the teams name"""

    url = 'https://api.nhle.com/stats/rest/en/team'
    response = requests.get(url)
    results = json.loads(response.text)
    teams = []

    for team in results['data']:
        teams.append(team['fullName'])
    
    
    return teams


def get_team_id(team_name):
    """ Function to get team of user and return NHL team ID"""

    url = 'https://api.nhle.com/stats/rest/en/team'
    response = requests.get(url)
    results = json.loads(response.text)

    for team in results['data']:
        if team['fullName'] == team_name:
            return team['triCode']

    raise Exception("Could not find ID for team {0}".format(team_name))


def fetch_score(team_id):
    """ Function to get the score of the game depending on the chosen team.
    Inputs the team ID and returns the score found on web. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    url = '{0}scoreboard/{1}/now'.format(NHL_API_URL, team_id)
    # Avoid request errors (might still not catch errors)
    
    try:
        score = requests.get(url)
        score = json.loads(score.text)
        
        #game_time = str(score['dates'][0]['games'][0]['teams'])
        #print (game_time)

        for status in score['gamesByDate']:
            #print(status['games'][0]['gameState']," ",status['date'])
            if status['games'][0]['gameState'] == 'LIVE' or status['games'][0]['gameState'] == 'CRIT':
                if team_id == status['games'][0]['homeTeam']['abbrev']:
                    score = int(status['games'][0]['homeTeam']['score'])
                    break
                else:
                    score = int(status['games'][0]['awayTeam']['score'])
                    break
            else:
                score = 0
                

        # Print score for test
        print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second),end='\r')

        return score

    except requests.exceptions.RequestException:
        print("Error encountered, returning 0 for score")
        return 0


def check_game_status(team_id,date):
    """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """
    # Set URL depending on team selected and date
    url = '{0}club-schedule/{1}/week/{2}'.format(NHL_API_URL, team_id, date)

    try:
        #get game state from API (no state when no games on date)
        game_status = requests.get(url)
        game_status = json.loads(game_status.text)
        game_status = game_status['games'][0]['gameState']
        
        "print(game_status)"
        return game_status

    except IndexError:
        #Return No Game when no state available on API since no game
        return 'No Game'

    except requests.exceptions.RequestException:
        # Return No Game to keep going
        return 'No Game'


def get_next_game_date(team_id):
    "get the time of the next game"
    date_test = datetime.date.today()
    gameday = check_game_status(team_id,date_test)

    #Keep going until game day found
    while ("FUT" not in gameday):
        date_test = date_test + datetime.timedelta(days=1)
        gameday = check_game_status(team_id,date_test)

    #Get start time of next game
    url = '{0}club-schedule/{1}/week/{2}'.format(NHL_API_URL, team_id,date_test)
    utc_game_time = requests.get(url)
    utc_game_time = json.loads(utc_game_time.text)
    utc_game_time = utc_game_time['games'][0]['startTimeUTC']
    next_game_time = convert_to_local_time(utc_game_time) - datetime.timedelta(seconds=30)

    return next_game_time

def convert_to_local_time(utc_game_time):
    "convert to local time from UTC"
    utc_game_time = datetime.datetime.strptime(utc_game_time, '%Y-%m-%dT%H:%M:%SZ')
    utc_game_time = utc_game_time.replace(tzinfo=tz.tzutc())
    local_game_time = utc_game_time.astimezone(tz.tzlocal())

    return local_game_time
