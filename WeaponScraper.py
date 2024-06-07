# Scraping Datasheets for WH40K experiment

import pandas as pd
import pymupdf
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




fff = "Necrons"
# for faction in factions: 
main_path = r"C:\\Users\\Chonky Boi\\Documents\\Python Scripts\\Datasets\\40K_Datasheets\\" 
doc_path = main_path + fff + ".pdf" #faction
csv_path = main_path + "Basic_Unit_Stats\\" + fff + ".csv"
new_path = main_path + fff


try:
    # Open the PDF file
    doc = pymupdf.open(doc_path)
    
    # Check if the document is encrypted
    if doc.is_encrypted:
        print("The document is encrypted.")
    else:
        print("The document is not encrypted.")
    
    # Check the number of pages
    num_pages = doc.page_count
    print(f"Number of pages in the document: {num_pages}")
    
    if num_pages > 0:
        # Try to load the first page
        page_number = 0  # First page index is 0
        try:
            page = doc.load_page(page_number)
            print(f"Successfully loaded page {page_number + 1}.")
        except Exception as e:
            print(f"Failed to load page {page_number + 1}: {e}")
    else:
        print("The document has no pages.")
        
except Exception as e:
    print(f"An error occurred while opening the document: {e}")


page_ids = []
wpon_list = []

pattern1 = r'\n'
pattern2 = r'RANGED WEAPONS'
pattern3 = r'MELEE WEAPONS'

def get_page_size(doc, page_number):
    # Load the page
    page = doc.load_page(page_number)
    
    # Get the MediaBox of the page
    media_box = page.mediabox
    
    # Extract the width and height
    width = media_box[2] - media_box[0]
    height = media_box[3] - media_box[1]
    
    return width, height

width, height = get_page_size(doc,6)


# Extraction Starts here
if width/height > height/width:
    print("Wide page")
    print('width/height',width/height )
    print('height/width',height/width )
    
    for i in range(6,len(doc)-1):

        buggered_lists = []

        page = doc.load_page(i)  # number of page

        text = page.get_text()
        

        mod_text = re.sub(pattern1,' ',text) # removing newlines
        
        # print(text)

        index1 = text.find(pattern2)
        index2 = text.find(pattern3) # TODO: add conditional if there's no melee weapons, need new indexer?

        # if index2 == -1:

        
        stats_and_names = text[ index1 + len(pattern2): index2]
        
        #split entries by newlines into list?
        stats_and_names = stats_and_names.split('\n')
        
        
        if i%2 == 0:
            
            
            print(f"\n USEFUL DATA page {i}\n ")

            print(f'stats and names \n\n', stats_and_names)
            print(f"\n\nLength of stats and names data extracted" , len(stats_and_names))

            stats_and_names = stats_and_names[7:-1] #remove extra bit
            print(stats_and_names)

          
            print('length of loop',len(stats_and_names)/7)
                        
            if len(stats_and_names)%7 != 0: # detecting problem loops and investigating if there's a pattern
                print('Problem in the string exists. Data extracted here:')
                buggered_lists.append([page,stats_and_names])

            else:
                for j in range(0,int(len(stats_and_names)/7)):
                    wpon_list.append(stats_and_names[j*7:j*7+7])


            print(f'\n\n saved data \n\n')
            print(wpon_list)
            print(f'\n\n')

            print(f"Problematic lists and their page in first col \n\n")


            for i in range(len(buggered_lists)):
                a = buggered_lists[i]
                print(buggered_lists[i])
                print(f'length of loop \n',len(a[1])/7)
                print(f'on page \n', a[0])
            

        else:
            print(f'\n\n BS PAGE DETECTED: page {i}\n')
        

        
        #TODO: 

        # Some weapons got that extra \n in front of the attribute list. need to figure out how to
        # 1. detect that
        # 2. squish the names together
        # 3. append

        # save data into csv
        # figure out how to add unit names to each piece of data? probably by extracting text from the beginning of each page that includes unit name, and then appending it to each row that's generated.

else:  
    print('long page')
    
    buggered_lists = []
    for i in range(6,len(doc)-1): # range(6,len(doc)-1):
        
        page = doc.load_page(i)  # number of page

        text = page.get_text()

        # print("Extracted text", text)
        mod_text = re.sub(pattern1,' ',text) # removing newlines
        
        # print(text)

        index1 = text.find(pattern2)
        index2 = text.find(pattern3)# TODO: add conditional if there's no melee weapons, need new indexer?
        
        stats_and_names = text[ index1 + len(pattern2): index2]
        
        #split entries by newlines into list?
        stats_and_names = stats_and_names.split('\n')
        
        
        
        print(f"\n USEFUL DATA page {i}\n ")

        print(f'stats and names \n\n', stats_and_names)
        print(f"\n\nLength of stats and names data extracted" , len(stats_and_names))

        stats_and_names = stats_and_names[7:-1] #remove extra bit
        

        
        print('length of loop',len(stats_and_names)/7)
        #the loop is ideally a multiple of 7 long.


        if len(stats_and_names)%7 != 0: # detecting problem loops and investigating if there's a pattern
            print('Problem in the string exists. Data extracted here:')
            buggered_lists.append([page,stats_and_names])

        else:
            for j in range(0,int(len(stats_and_names)/7)):
                wpon_list.append(stats_and_names[j*7:j*7+7])
            
        


        # The bullshit lists are gonna be saved here into a separate csv.
        # gonna edit that in post
        print(f"Problematic lists and their page in first col \n\n")

        for i in range(len(buggered_lists)):
            a = buggered_lists[i]
            print(buggered_lists[i])
            print(f'length of loop \n',len(a[1])/7)
            print(f'on page \n', a[0])
        
print(wpon_list)
doc.close()



#converting document to pages

## __________ EXTRACTION CODE
# wpon_list = []


# table_headers = ["Name" , "Range", "A", "WS", "S", "AP", "P","Related Unit"]
    
# df = pd.DataFrame(wpon_stats, columns = table_headers)
# print(df.head(10))
# df.to_csv(r"C:\\Users\\Chonky Boi\\Documents\\Python Scripts\\Datasets\\40K_Datasheets\\" + fff + ".csv", index = False)
