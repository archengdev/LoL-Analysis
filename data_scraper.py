
from csv import writer, DictReader

import pandas as pd
from sortedcontainers import SortedList
import arrow
import cassiopeia as cass

from private import API_KEY

# get list of match id's that have already been looked at
seen_ids = SortedList()
with open('aram_damage_data.csv', 'r') as data:
    file = DictReader(data)

    # get match_id from each column, and add to the list
    for col in file:
        seen_ids.add(int(col['match_id']))

# maybe move file outside? if opening and closing takes a while
def add_to_csv(match):
    """
    takes a cass match object and adds relevant data to csv
    adds match id, and:
    champ name, magic damage dealt, physical damage dealt, damage mitigated
    for each of the 10 players
    """
    lst = [match.id]
    for player in match.participants:
        lst.append(player.champion.name)
        stats = player.stats
        lst.append(stats.magic_damage_dealt_to_champions)
        lst.append(stats.physical_damage_dealt_to_champions)
        lst.append(stats.damage_self_mitigated)
    with open('aram_damage_data.csv', 'a', newline='') as file:
        writer_obj = writer(file)
        writer_obj.writerow(lst)
        file.close()

# def filter_match_history(puuid, patch):
#     """
#     puuid: player id
#     patch: cass.Patch value
#     filters for ARAM games played by the given player on the current patch
#     """
#     end_time = patch.end
#     if end_time is None:
#         end_time = arrow.now()
#     match_history = cass.MatchHistory(puuid=puuid, queue={cass.Queue.aram}, 
#                                       start_time=patch.start, end_time=end_time)
#     return match_history


# set the api key
cass.set_riot_api_key(API_KEY)
cass.print_calls(False)

# create initial cassiopieia summoner object to begin API crawl from
account = cass.get_account(name="Bobybybob", tagline="6552", region="NA")
summoner = account.summoner

# choose a patch to analyse games for
patch = cass.Patch.from_str("9.19", region="NA")

# create a sorted list for player ID's (starting from the initial summoner) 
unseen_puuids = SortedList([summoner.puuid])
seen_puuis = SortedList()

# create a sorted list for ARAM match ID's to crawl through
unseen_ids = SortedList()

# number of matches to pull
num_matches = 100

# while unseen_ids and len(seen_ids) < num_matches:
    # get a random summoner from our list, and pull their match history

    # need: id, 

# filter_match_history(summoner.puuid, patch)
match_history = cass.get_match_history(puuid=summoner.puuid, start_time = patch.start, end_time= arrow.now(), queue=cass.Queue.aram, continent=summoner.region.continent )
print(match_history)
match = match_history[0]
print(type(match.id))
print(match.participants[0].champion)
S1_stats = match.participants[0].stats
print(match.id, match.participants[0].champion.name, S1_stats.magic_damage_dealt_to_champions, S1_stats.physical_damage_dealt_to_champions, S1_stats.damage_self_mitigated)

# for i in match_history:
#     print(i.id)
# print("matchID:", match.id)
# new_match = cass.Match(id=match, region="NA")
# print(new_match)



# while unseen_ids and len(seen_ids) < num_matches:
    # get a random summoner from our list, and pull their match history

    # need: id, 
# filter_match_history(summoner.puuid, patch)
# match_history = cass.get_match_history(puuid=summoner.puuid, start_time = patch.start, end_time= arrow.now(), queue=cass.Queue.aram, continent=continent)
# print(match_history)
# match = match_history[0]
# print(type(match.id))
# print(match.participants[0].champion)
# S1_stats = match.participants[0].stats
# print(match.id, match.participants[0].champion.name, S1_stats.magic_damage_dealt_to_champions, S1_stats.physical_damage_dealt_to_champions, S1_stats.damage_self_mitigated)

# for i in match_history:
#     print(i.id)
# print("matchID:", match.id)
# new_match = cass.Match(id=match, region="NA")
# print(new_match)