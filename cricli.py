#!/usr/local/bin/python
import requests
import json
import argparse
import pprint
import threading
from time import sleep

#cric api related info.
data = {'apikey':'GRHrEG8UCofaZgNzciuDKvtyV0A3'}
scores_data = {}
score_data = {}
list_of_matches=[]
display_options =['TRUE','FALSE','ALL','INDIVIDUAL']
print_string = " " + "-"*40
tab_string = " "*25

# Fetches
def store_matches(matches):
    index = 0
    for match in matches:
        for m in matches[match]:
            list_of_matches.insert(index,m)
            index = index +1
    return list_of_matches

# Creates a list of matches keyed.
def fetch_matches():
    match_url = 'http://cricapi.com/api/matches/'
    r = requests.post(match_url,data)
    matches = r.json()
    list_of_matches = store_matches(matches)
#fetch_scores()

# Creates a dictionary of match scores keyed on match id..
def fetch_scores(match_id):
    score_url = 'http://cricapi.com/api/cricketScore/'
    if match_id is 0:
        for match in list_of_matches:
            sleep(0.5)
            data['unique_id'] = match['unique_id']
            r = requests.post(score_url,data)
            scores_data[ match['unique_id']] = r.json()
            return scores_data
    else:
        data['unique_id'] = match_id 
        r = requests.post(score_url,data)
        score_data = r.json()
        return score_data
         

def spawn_workers_and_do_work():
    thread1 = threading.Thread(target=fetch_matches)
    thread1.start()

def display_scores(option_string,match_id):
    if option_string in display_options and option_string is 'ALL':
        print 'Going to display all scores'
    if option_string in display_options and option_string is 'INDIVIDUAL':
        score_data = fetch_scores(match_id)
        matchid_string = " Match - " + str(match_id)
        team_string = score_data['team-1'] + " vs " + score_data['team-2']
        print print_string + matchid_string + print_string
        print tab_string + team_string 
        print tab_string + "-"*len(team_string) 
        print " SCORE :: " + score_data['score']
        print " REQUIREMENT :: " + score_data['innings-requirement']
        print print_string + "-"*len(matchid_string) + print_string
    
def display_matches(option_string):
    print print_string + print_string
    print tab_string + " List of current matches "
    print print_string + print_string
    if option_string in display_options:
       if option_string == 'ALL':
           for match in list_of_matches:
               print 'Match - ' + str(match['unique_id']) + ' :: ::  ' + match['team-1'] + ' vs ' + match['team-2']  + ' :: :: Match Started: ' + str(match['matchStarted'])
       elif option_string == 'TRUE':
           for match in list_of_matches:
               if match['matchStarted'] is True:
                   print 'Match - ' + str(match['unique_id']) + ' :: ::  ' + match['team-1'] + ' vs ' + match['team-2']  + ' :: :: Match is underway. '
       elif option_string == 'FALSE':
           for match in list_of_matches:
               if match['matchStarted'] is False:
                   print 'Match - ' + str(match['unique_id']) + ' :: ::  ' + match['team-1'] + ' vs ' + match['team-2']  + ' :: :: Match has not started yet.  '

#setup argument parser
def parse_some_args():
    parser = argparse.ArgumentParser(description='CLI to fetch latest cricket scores from around the globe!')
    parser.add_argument('-m','--matches',action="store_true",help='Matches scheduled to start shortly')
    parser.add_argument('-mt','--matches-true',dest="match_true",action="store_true",help='Matches currently underway')
    parser.add_argument('-mf','--matches-false',dest="match_false",action="store_true",help='Matches yet to begin ')
    parser.add_argument('-s','--score',dest="match_id",help='Enter the game id to see the score')
    parser.add_argument('-sa','--score-all',dest="score_all",help='Display scores for all ongoing games')
    args = parser.parse_args()
    
    if args.matches:
        display_matches('ALL')
    if args.match_true:
        display_matches('TRUE')
    if args.match_false:
        display_matches('FALSE')
    if args.match_id:
        display_scores('INDIVIDUAL',args.match_id)
    if args.score_all:
        display_scores('ALL',0)

if __name__=='__main__':
#spawn_workers_and_do_work()
    fetch_matches()
    parse_some_args()
