
from csv import writer, DictReader

import random
import pandas as pd
from sortedcontainers import SortedList
import arrow
import cassiopeia as cass

from private import API_KEY

# get list of match id's that have already been looked at
seen_match_ids = SortedList()
with open('aram_damage_data.csv', 'r') as data:
    file = DictReader(data)

    # get match_id from each column, and add to the list
    for col in file:
        seen_match_ids.add(int(col['match_id']))

# maybe move file outside? if opening and closing takes a while
def add_to_csv(match, writer_obj):
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
    writer_obj.writerow(lst)

# set the api key
cass.set_riot_api_key(API_KEY)
cass.print_calls(False)

# create initial cassiopieia summoner object to begin API crawl from
account = cass.get_account(name="SirFlash", tagline="NA1", region="NA")
summoner = account.summoner

# choose a patch to analyse games for
patch = cass.Patch.from_str("9.19", region="NA")

# create a sorted list for player ID's (starting from the initial summoner) 
unseen_puuids = SortedList([summoner.puuid])
seen_puuis = SortedList()

# create a sorted list for ARAM match ID's to crawl through
unseen_matches = []

ctnt = summoner.region.continent
# number of matches to pull
num_matches = 100000

with open('aram_damage_data.csv', 'a', newline='') as file:
    writer_obj = writer(file)
    
    while unseen_puuids and len(seen_match_ids) < num_matches:
        # get a random summoner from our list, and pull their match history
        new_puuid = random.choice(unseen_puuids)

        # get the ARAM matches from their history
        matches = cass.get_match_history(puuid = new_puuid,
                                        start_time = patch.start,
                                        end_time = arrow.now(),
                                        queue = cass.Queue.aram,
                                        continent = ctnt)
        
        # add each match to our unseen list
        for match in matches:
            if match.id not in seen_match_ids:
                unseen_matches.append(match)

        # update puuid lists
        unseen_puuids.remove(new_puuid)
        seen_puuis.add(new_puuid)
        print(unseen_puuids)

        # loop over all unseen matches, and add info to csv
        while unseen_matches and len(seen_match_ids) < num_matches:
            # get a match from unseen matches
            match = unseen_matches.pop()
            currID = match.id

            # use try - except to continue when API calls fail
            try:
                # loop over all participants, add them to our unseen list (if unseen)
                for p in match.participants:
                    if p.summoner.puuid not in seen_puuis:
                        unseen_puuids.add(p.summoner.puuid)

                # add match data to the csv
                add_to_csv(match, writer_obj)
            except:
                print(currID, "failed")

            # add current ID to seen matches
            seen_match_ids.add(currID)

            # check progress
            if len(seen_match_ids) % 100 == 0:
                print(len(seen_match_ids))

    file.close()
# filter_match_history(summoner.puuid, patch)
# match_history = cass.get_match_history(puuid=summoner.puuid, start_time = patch.start, end_time= arrow.now(), queue=cass.Queue.aram, continent=ctnt )
# with open('aram_damage_data.csv', 'a', newline='') as file:
        
#         for match in unseen_matches:
#             add_to_csv(match, writer_obj)
#             print("done")
#         file.close()
# for match in unseen_matches:
#     currID = match.id
#     try:
#         for p in match.participants:
#             print(p.summoner.puuid)
#     except:
#         print(currID, "failed")
quit()

match = random.choice(unseen_matches)
S1_stats = match.participants[0].stats
print(match.id, match.participants[0].champion.name, S1_stats.magic_damage_dealt_to_champions, S1_stats.physical_damage_dealt_to_champions, S1_stats.damage_self_mitigated)
print(match.participants[1].summoner.puuid)
# for i in match_history:
#     print(i.id)
# print("matchID:", match.id)
# new_match = cass.Match(id=match, region="NA")
# print(new_match)