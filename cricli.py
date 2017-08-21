#!/usr/local/bin/python
import requests
import json
import argparse
import pprint
import datetime
from time import sleep
from collections import defaultdict


# Fetches
class Cricket():
    def __init__(self):
        self.api_key = {'apikey':'GRHrEG8UCofaZgNzciuDKvtyV0A3'}
        self.score_data = {}
        self.list_of_matches = [] # a list of dictionaries
        self.match_url = 'http://cricapi.com/api/matches/'
        self.score_url = 'http://cricapi.com/api/cricketScore/'
        self.collect_matches()

    def store_matches(self,match_data):
        ''' Store match information for retrieval later on '''
        index = 0
        # match_data is a dictionary of dictionaries
        for key,matches in match_data.iteritems():
            if key == 'matches':
                # extract each match and put it in a list_of_matches
                for match in matches:
                    self.list_of_matches.append(match)

        # Creates a list of matches keyed.
    def collect_matches(self):
        r = requests.post(self.match_url,self.api_key)
        matches = r.json()
        self.store_matches(matches)

        # Creates a dictionary of match scores keyed on match id..
    def get_score(self,match_id):
        data['unique_id'] = match_id
        r = requests.post(self.score_url,data)
        score_data = r.json()
        return score_data

    def get_total_matches(self):
        return len(self.list_of_matches)

    def get_total_ongoing_matches(self):
        # For each match in list_of_matches
        # If the squad field is true, then count that
        # against total ongoing matches.
        _ongoing_match_count = 0
        for match in self.list_of_matches:
            for key,value in match.iteritems():
                if key == 'squad':
                    if value == True:
                        _ongoing_match_count = _ongoing_match_count +1
        return _ongoing_match_count

    def get_ongoing_matches(self):
        ongoing_matches = []
        for match in self.list_of_matches:
            for key, value in match.iteritems():
                if key == 'squad':
                    if value == True:
                        ongoing_matches.append(match)

        return ongoing_matches

    def dump_all(self):
        for match in self.list_of_matches:
            print match


#Test Driver
if __name__=='__main__':
#spawn_workers_and_do_work()
    crick = Cricket()
    crick.dump_all()
    print "Total cricket matches: " +str(crick.get_total_matches())
    print "Total ongoing cricket matches: " +str(crick.get_total_ongoing_matches())
