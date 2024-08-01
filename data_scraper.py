# import pandas as pd
# import requests
# from google.colab import files
from private import API_KEY

# df = pd.DataFrame()

import random
from sortedcontainers import SortedList
import arrow
import cassiopeia as cass

# from cassiopeia.core import Summoner, MatchHistory, Match
# from cassiopeia import Queue, Patch

cass.set_riot_api_key(API_KEY)
# account = cass.get_account(name="Kalturi", tagline="NA1", region="NA")
# summoner = account.summoner
# print(account.name_with_tagline, summoner.level, summoner.region)

# This function helps filter only aram matches for patch 9.19
def filter_match_history(puuid, patch):
    end_time = patch.end
    if end_time is None:
        end_time = arrow.now()
    match_history = cass.MatchHistory(puuid=puuid, queue={cass.Queue.aram}, start_time=patch.start, end_time=end_time)
    return match_history


# Intial summoner
initial_summoner_name = "Bobybybob"
region = "NA"

# create cassiopieia summoner object
account = cass.get_account(name="Kalturi", tagline="NA1", region="NA")
summoner = account.summoner
patch = cass.Patch.from_str("9.19", region=region)

# create a sorted list for player ID's (we start with the initial summoner name) 
unpulled_summoner_ids = SortedList([summoner.id])
pulled_summoner_ids = SortedList()

# create a sorted list for ARAM match ID's 
unpulled_match_ids = SortedList()
pulled_match_ids = SortedList() # This is the list of interest

# number of matches you want pulled
num_matches = 100

# filter_match_history(summoner.puuid, patch)
match_history = cass.get_match_history(puuid=summoner.puuid, start_time = patch.start, end_time= arrow.now(), queue=cass.Queue.aram, continent=summoner.region.continent )
print(match_history)
match = match_history[0]
print("matchID:", match.id)