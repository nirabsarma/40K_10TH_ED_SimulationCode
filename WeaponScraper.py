# Scraping Datasheets for WH40K experiment

import numpy as np
import pandas as pd
from pypdf import PdfReader
import re

# Basic Idea Here:

# I want to extract the unique ranged and melee weapons and their stats for each faction. 

# 1. create empty list of ranged weapons
# 2. iterate through list in csv file, so that unit names are easy to find.
# 3. check if weapon found is in list
# 4. if not, add to list, else, don't
# 5. check unit name list associated with each weapon
# 6. if the unit name is not in the list, add it in

# 1. create empty list of melee weapon_str
# 2. check if weapon found is in list
# 3. if not, add to list, else, don't
# 4. check unit name list associated with each weapon
# 5. if the unit name is not in the list, add it in





fff = "SpaceMarines"
# for faction in factions: 
doc_path = r"C:\\Users\\Chonky Boi\\Documents\\Python Scripts\\Datasets\\40K_Datasheets\\" + fff + ".pdf" #faction
csv_path = r"C:\\Users\\Chonky Boi\\Documents\\Python Scripts\\Datasets\\40K_Datasheets\\good_ones\\" + fff + ".csv"

pattern = "(?<=RANGED WEAPONS RANGE A BS S AP D)[\s\S]*?(?=MELEE WEAPONS RANGE A WS S AP D)"



reference_table = pd.read_csv(csv_path)
print(reference_table.head(4))

## __________ EXTRACTION CODE


reader = PdfReader(doc_path)

names = reference_table['Name'] # returns a pd series
names = pd.Series.to_list(names)

# Process matches

def weapons_detec(pattern, text): 

    matches = re.findall(pattern, text)
    objects_list = []
    for match in matches:
        # Split each match into lines
        lines = match.strip().split('\n')
        # Initialize a dictionary to store object statistics
        object_stats = {}
        # Iterate over lines to extract statistics
        for line in lines:
            # Split line by whitespace
            stats = line.split()
            # Check if there are statistics
            print("last 6 elements of stats",stats[-6:])
            if len(stats) >= 2:
                # Extract name and statistics
                if 'FLAMER' in stats:
                    print('Flamer alert? Or maybe extra newline found')
                else:
                    name = ' '.join(stats[:-6])  # Object name (excluding the last 6 elements which are statistics)
                    stats_values = stats[-6:]     # Object statistics
                
                if i == 100:
                    print(text)
                    print(name)
                print("pre-mod",stats_values)
                stats_values[0] = str(stats_values[0])[0:2]
                stats_values[2] = str(stats_values[2])[0]
                #remove stats values 
                print("post mod",stats_values)
                # Store name and statistics in the dictionary
                object_stats[name.strip()] = stats_values
        # Append the dictionary to the objects list
        objects_list.append(object_stats)

    # # Print the list of objects
    # for i, obj in enumerate(objects_list, 1):
    #     print(f"Object {i}:")
    #     for name, stats in obj.items():
    #         print(f"Name: {name}, Statistics: {stats}")

    return objects_list






wpon_list = []

for i in range(6,len(reader.pages)):
    
    page = reader.pages[i]
 
 
    print("Page Number", i )
    text = page.extract_text(extraction_mode = "plain")


    wpon_stats = weapons_detec(pattern, text)
    print(wpon_stats)
    if len(wpon_stats) > 0:

    # print(wpon_stats)
        wpons = list(wpon_stats[0].keys())
        stats = list(wpon_stats[0].values())
        print(wpons)
        print(stats)
        # print(stats[0])
        for i in range(0,len(wpons)):
            stats[i].insert(0, wpons[i])
            wpon_list.append(stats[i])
        # print(wpon_list)
    # if len(wpon_list[-1] < )
    # by the end of this loop, we've got all the weapons on the page into the list.
    # but we still need to add to add in the unit check
        
    # if the weapon is in the list, add the name of the unit to the relevant weapon unit list
    # if the weapon is not in the list, then add the weapon in


print(wpon_list)


# now making this into a pd dataframe

table_headers = ["Name" , "Range", "A", "WS", "S", "AP", "P","Related Unit"]
    
df = pd.DataFrame(wpon_stats, columns = table_headers)
print(df.head(10))
df.to_csv(r"C:\\Users\\Chonky Boi\\Documents\\Python Scripts\\Datasets\\40K_Datasheets\\" + fff + ".csv", index = False)
