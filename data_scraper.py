import pandas as pd
# import requests
# from google.colab import files
from private import API_KEY

# df = pd.DataFrame()

import random
from sortedcontainers import SortedList
import arrow
import cassiopeia as cass


# set the api key
cass.set_riot_api_key(API_KEY)

def filter_match_history(puuid, patch):
    """
    puuid: player id
    patch: cass.Patch value
    filters for ARAM games played by the given player on the current patch
    """
    end_time = patch.end
    if end_time is None:
        end_time = arrow.now()
    match_history = cass.MatchHistory(puuid=puuid, queue={cass.Queue.aram}, 
                                      start_time=patch.start, end_time=end_time)
    return match_history


# create initial cassiopieia summoner object to begin API crawl from
account = cass.get_account(name="Bobybybob", tagline="6552", region="NA")
summoner = account.summoner
patch = cass.Patch.from_str("9.19", region="NA")

# create a sorted list for player ID's (we start with the initial summoner name) 
unpulled_puuids = SortedList([summoner.puuid])
pulled_puuis= SortedList()

# create a sorted list for ARAM match ID's 
unpulled_match_ids = SortedList()
pulled_match_ids = SortedList() # This is the list of interest

# number of matches you want pulled
num_matches = 100

# filter_match_history(summoner.puuid, patch)
match_history = cass.get_match_history(puuid=summoner.puuid, start_time = patch.start, end_time= arrow.now(), queue=cass.Queue.aram, continent=summoner.region.continent )
print(match_history)
match = match_history[0]
print(match.participants[0].champion)
print(match.participants[0].stats.magic_damage_dealt)
# for i in match_history:
#     print(i.id)
# print("matchID:", match.id)
# new_match = cass.Match(id=match, region="NA")
# print(new_match)