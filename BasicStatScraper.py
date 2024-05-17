# Scraping Datasheets for WH40K experiment

import numpy as np
from pypdf import PdfReader
import re
import pandas as pd

factions = ['SpaceMarines','AstraMilitarum','Orks',"ChaosDemons", "Necrons", "Tau","Tyranids"]

fff = "AstraMilitarum"

# for faction in factions: 
path = r"C:\\Users\\Chonky Boi\\Documents\\Python Scripts\\Datasets\\40K_Datasheets\\" + fff + ".pdf" #faction


reader = PdfReader(path)


def num_after_substr(input_string, substring):
    # Find the index of the substring
    start_index = input_string.find(substring)
    
    # Extract the substring after the occurrence of the substring
    if start_index != -1:
        substring_after = input_string[start_index + len(substring):]
        
        # Use regular expression to find all numbers
        numbers = re.findall(r'\d+', substring_after)
        
        return numbers
    else:
        return []
    

def num_in_range(input_string, start_string,stop_string):
    # Find the index of the substring
    start_index = input_string.find(start_string)
    stop_index = input_string.find(stop_string)
    # Extract the substring after the occurrence of the substring

    if start_index != -1:
        substring = input_string[start_index:stop_index]
        # Use regular expression to find all numbers
        numbers = re.findall(r'\d+', substring)
        
        return numbers
    else:
        return []

#strings for sampling number data
profile_str = "M T SV W LD OC" # this is the string i want to check for. any numbers after this, I want to save, in order
weapon_str = "RANGED WEAPONS RANGE A BS S AP D"
melee_str = "MELEE WEAPONS RANGE A WS S AP D"
Invuln_save = "INVULNERABLE SAVE"
Name_START = "KEYWORDS"
Name_END = "FACTION KEYWORDS"
MoreNonsense = "Balance Dataslate January 2024"
stats_table = []
weapon_table = []


oddities = []


for i in range(6,len(reader.pages)):
    
    page = reader.pages[i]
    
    
    print("Page Number", i )


    text = page.extract_text(extraction_mode = "plain")

    unit_stats = num_after_substr(text, profile_str)
    unit_stats = unit_stats[0:6]
    
    wpon_stats = num_in_range(text,weapon_str,melee_str)
        
    invuln = num_in_range(text,Invuln_save,profile_str)
    

    if len(unit_stats) > 0:
        print("Stats were found on this page")
        print(unit_stats)
        
    if len(unit_stats) > 0 and len(unit_stats) < 6: #length of list < 6, unit has no movement, append 0 
        unit_stats.insert(0, 0)
        



    if len(unit_stats) > 0: #unit stats exist, insert the unit name.

        unit_name = text[0:80]

        print("Raw data for Unit Name --- \n \n", str(unit_name))

        start_of_name = unit_name.find(MoreNonsense)
        end_of_name = unit_name.find('\n')
        alt1 = unit_name.find(Name_START)     
        
        print("name start ind" ,start_of_name)
        print("name end ind",end_of_name)
        print("name end altind", alt1)
        if start_of_name != -1 and  alt1 != -1:
            unit_name = unit_name[start_of_name+len(MoreNonsense):alt1]
        elif start_of_name != -1 and  end_of_name != -1:
            unit_name = unit_name[start_of_name+len(MoreNonsense):end_of_name]
        elif start_of_name == -1 and end_of_name != -1:
            unit_name = unit_name[0:end_of_name]

        elif start_of_name == -1 and end_of_name == -1:
           unit_name = unit_name[0,alt1]

        print(unit_name)
        unit_stats.insert(0, unit_name[0:len(unit_name)-2])


    if len(invuln) > 0 and len(unit_stats) == 7: #invuln save exists, add to list,  else   NaN
        print("This unit has an invuln save", invuln)
        unit_stats.append(invuln[0])
    else:
        unit_stats.append("NaN")

    if len(unit_stats) > 8 or unit_stats[0] == "":
        print(f"\n \n \n RAW TEXT \n \n ",text)
        print(f"\n \n \n Unit Stats Produced: \n \n ",unit_stats)
        print("\n \n Page number", i)
        raise Exception("Something broke here, check out the text")
    print("Unit stats after some shenanigans")
    print(unit_stats)

    if unit_stats == None:
        print("No data on page")
    elif len(unit_stats) == 8: # this deals with regular units and most vehicles like bikes, planes bla bla
        stats_table.append(unit_stats)

# now making this into a pd dataframe
table_headers = ["Name" , "M", "T", "SV", "W", "LD", "OC","ISV"]

df = pd.DataFrame(stats_table, columns = table_headers)
print(df.head(24))

df.to_csv(r"C:\\Users\\Chonky Boi\\Documents\\Python Scripts\\Datasets\\40K_Datasheets\\" + fff + ".csv", index = False)
