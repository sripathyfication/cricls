#!/usr/local/bin/python
import requests
import json
import argparse
import pprint
import datetime
from time import sleep
from collections import defaultdict

#cric api related info.
data = {'apikey':'GRHrEG8UCofaZgNzciuDKvtyV0A3'}
scores_data = defaultdict()
score_data = {}
list_of_matches=[]
display_options =['TRUE','FALSE','ALL','INDIVIDUAL', 'SUMMARY']
print_string = "."
tab_string = " "*25
match_url = 'http://cricapi.com/api/matches/'
score_url = 'http://cricapi.com/api/cricketScore/'

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
    r = requests.post(match_url,data)
    matches = r.json()
    list_of_matches = store_matches(matches)
#fetch_scores()

# Creates a dictionary of match scores keyed on match id..
def fetch_scores(match_id):
    data['unique_id'] = match_id 
    r = requests.post(score_url,data)
    score_data = r.json()
    return score_data
         
def display_scores(option_string,match_id):
    if (option_string in display_options) and (option_string is 'SUMMARY'):
        print print_string*len(tab_string + "Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + tab_string)
        print tab_string + "Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        print tab_string + print_string*len("Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        for match in list_of_matches:
            if match['matchStarted'] is True:
                score_data = fetch_scores(match['unique_id'])
                print match['team-1'] + ' vs ' + match['team-2']  + ' :::: ' + score_data['score']
                print tab_string + print_string*len("Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    if (option_string in display_options) and (option_string is 'INDIVIDUAL'):
        score_data = fetch_scores(match_id)
        team_string = score_data['team-1'] + " vs " + score_data['team-2']
        print print_string*len(tab_string + "Match  :-  " + str(match_id) + " " + team_string + " " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + tab_string) 
        print tab_string + "Match  :-  " + str(match_id) + " " + team_string + " " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        print tab_string + print_string*len("Match  :-  " + str(match_id) + " " + team_string + " " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        print " Score :- " + score_data['score']
        print " REQUIREMENT :- " + score_data['innings-requirement']
        print print_string*len(tab_string + "Match  :-  " + str(match_id) + " " + team_string + " " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + tab_string) 
    
def display_matches(option_string):
    print print_string*len(tab_string + "Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + tab_string)
    print tab_string + "Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    print tab_string + print_string*len("Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    if option_string in display_options:
       if option_string == 'ALL':
           for match in list_of_matches:
               print 'Match - ' + str(match['unique_id']) + ' :: ::  ' + match['team-1'] + ' vs ' + match['team-2']  + ' :: :: Match Started: ' + str(match['matchStarted'])
               print tab_string + print_string*len("Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
       elif option_string == 'TRUE':
           for match in list_of_matches:
               if match['matchStarted'] is True:
                   print 'Match - ' + str(match['unique_id']) + ' :: ::  ' + match['team-1'] + ' vs ' + match['team-2']  + ' :: :: Match is underway. '
                   print tab_string + print_string*len("Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
       elif option_string == 'FALSE':
           for match in list_of_matches:
               if match['matchStarted'] is False:
                   print 'Match - ' + str(match['unique_id']) + ' :: ::  ' + match['team-1'] + ' vs ' + match['team-2']  + ' :: :: Match has not started yet.  '
                   print tab_string + print_string*len("Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    print print_string*len(tab_string + "Cricket Matches "  + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + tab_string)

#setup argument parser
def parse_some_args():
    match_true = False
    match_false = False
    match = False
    score = False
    score_true = False
    
    parser = argparse.ArgumentParser(description='CLI to fetch latest cricket scores from around the globe!')
    parser.add_argument('-m','--matches',action="store_true",help='Matches scheduled to start shortly')
    parser.add_argument('-mt','--matches-true',dest="match_true",action="store_true",help='Matches currently underway')
    parser.add_argument('-mf','--matches-false',dest="match_false",action="store_true",help='Matches yet to begin ')
    parser.add_argument('-s','--score',dest="match_id",help='Enter the game id to see the score')
    parser.add_argument('-st','--score-true',dest="score_true",action="store_true",help='Show in summary scores for all matches currently underway')
    args = parser.parse_args()
    
    # Get what options have been passed.
    if args.matches:
        match = True
    if args.match_true:
        match_true = True
    if args.match_false:
        match_false = True
    if args.match_id:
        score = True
    if args.score_true:
        score_true = True    

    if match and not (match_true and match_false and score):
        display_matches('ALL')
    elif score and not (match and match_true and match_false):    
        display_scores('INDIVIDUAL',args.match_id)
    elif match_true and not (match and score and match_false and score_true):
        display_matches('TRUE')    
    elif match_false and not (match and score and match_true and score_true):
        display_matches('FALSE')    
    elif score_true and not (match and score and match_true and match_false):
        display_scores('SUMMARY',0)

if __name__=='__main__':
#spawn_workers_and_do_work()
    fetch_matches()
    parse_some_args()
