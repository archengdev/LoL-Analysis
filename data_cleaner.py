from csv import writer, DictReader

# maybe everything can be replaced by column-wise multiplications and stuff?

# for each row in original data, add it to the processed data
with open("./9.19/test data.csv", "r") as to_read, open("./9.19/processed_data.csv", "a", newline="") as to_write:
    # create objects to read/write
    data = DictReader(to_read)
    writer_obj = writer(to_write)

    
    for row in data:
        winning_mag = winning_phy = winning_mit = winning_magphy = winning_phymit = winning_magphymit = 0
        losing_mag = losing_phy = losing_mit = losing_magphy = losing_phymit = losing_magphymit = 0

        # determines if there was an afk player in the game (skip this match if there was)
        afk = False

        # first 5 summoners are part of the winning team
        for i in range(1, 6):

            # set up query strings for each stat
            query_mag = "s" + str(i) + "_mag_dmg"
            query_phy = "s" + str(i) + "_phy_dmg"
            query_mit = "s" + str(i) + "_dmg_mit"
            mag, phy, mit = int(row[query_mag]), int(row[query_phy]), int(row[query_mit])

            # if total stats are less than 2000, good chance someone is afk
            if mag + phy + mit < 2000:
                afk = True
                break
        
            # add data 
            winning_mag += mag; winning_phy += phy; winning_mit += mit
            winning_magphy += mag * phy; winning_phymit += phy * mit
            winning_magphymit += mag * phy * mit
        
        if afk: break

        # repeat process for losing team
        for i in range(6, 11):
            # set up query strings for each stat
            query_mag = "s" + str(i) + "_mag_dmg"
            query_phy = "s" + str(i) + "_phy_dmg"
            query_mit = "s" + str(i) + "_dmg_mit"
            mag, phy, mit = int(row[query_mag]), int(row[query_phy]), int(row[query_mit])

            # if total stats are less than 2000, good chance someone is afk
            if mag + phy + mit < 2000:
                afk = True
                break
        
            # add data 
            losing_mag += mag; losing_phy += phy; losing_mit += mit
            losing_magphy += mag * phy; losing_phymit += phy * mit
            losing_magphymit += mag * phy * mit
        
        if afk: break

        lst = [row['match_id'], winning_mag, winning_phy, winning_mit, winning_magphy, winning_phy, winning_magphymit, losing_mag, losing_phy, losing_mit, losing_magphy, losing_phymit, losing_magphymit]
        writer_obj.writerow(lst)


    to_read.close()
    to_write.close()