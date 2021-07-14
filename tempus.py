import sys
import json
import requests

def display_map(mapname): # takes the full map name as a string parameter
    try: # attempt to send request
        resp = requests.get('https://tempus.xyz/api/maps/name/' + mapname + '/fullOverview') # query map overview info

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            m = json.loads(resp.text) # loads json as python dictionary
            print() # newline for formatting

            # print map name
            print(m["map_info"]["name"] + ' by ', end='') # end='' parameter to make print function not end with newline.
            
            # print map authors differently depending on how many of them there are
            if len(m["authors"]) == 0: # api returned no authors
                print('N/A')
            elif len(m["authors"]) == 1: # only one author; just print it
                print(m["authors"][0]["name"])
            elif len(m["authors"]) == 2: # print two authors joined by and
                print(m["authors"][0]["name"] + ' and ' + m["authors"][1]["name"])
            else: # for three or more, join all the authors with commar except for the last, joined by and
                numauthors = len(m["authors"]) # store number of authors in a variable

                for i in range(0, numauthors - 2): # for loop will iterate through all authors except the last 2
                    print(m["authors"][i]["name"] + ', ', end='') # end='' parameter to make print function not end with newline.
                
                print(m["authors"][numauthors-2]["name"]+' and '+m["authors"][numauthors-1]["name"]) # print the last two authors joined by 'and'
            
            # print tier info
            print('Solly T'+str(m["tier_info"]["soldier"])+' | Demo T'+str(m["tier_info"]["demoman"])) # tier info value must be casted to string in order to be printed
                
            # print course info
            if "linear" in m["zone_counts"]: # if map is linear, key "linear" will exist in the dictionary
                print('Linear, ', end='')
            else: # if it isn't linear, it will have courses
                print(str(m["zone_counts"]["course"]) + ' courses, ', end='')

            # print bonus info (if any)
            if "bonus" in m["zone_counts"]: # if there are bonuses, key "bonus" will exist
                print(str(m["zone_counts"]["bonus"]) + ' bonus', end='')
                if m["zone_counts"]["bonus"] > 1:  # if there is more than one bonus, it should print bonusES instead
                    print('es', end='')
                print() # newline for formatting
            else: # there are no bonuses
                print('no bonuses')

            print() # newline for formatting

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)

def choose_one_map(maps): # prompts user to choose one map from 2-5 results
    print(str(len(maps)) + ' partial matches found:')

    for i in range(0, len(maps)): # range() is used because the index number needs to be printed
        print(' ' + str(i+1) + '. ' + maps[i]["name"])

    index = input('Enter the number next to the map you wish to view (!q to go back): ')

    while index != '!q': # !q is the string that allows user to exit from the function

        if index in ['1','2','3','4','5']: # first make sure user inputted string that is a number between 1-5
            if int(index) <= len(maps): # since the prior statement ensures the input is an int between 1-5, the only other check is to make sure the index is not larger than the map query results
                display_map(maps[int(index)-1]["name"]) # the map info can be safely fetched
                break # after map info is displayed, return to search map function
            else: # the inputted index does not exist in the map result dictionary
                print('Invalid input, please enter one of the displayed numbers.')
        else: # user input is not an integer between 1-5
            print('Invalid input, please enter one of the displayed numbers.')
        
        index = input('Enter the number next to the map you wish to view (!q to go back): ') # reprint the input query for the loop
    
def search_map(): # handles looking up maps
    query = input('Search for a map (!q to go back): ').lower() # scanner to read input, convert to lower case

    while query != '!q': # !q is the string that allows user to exit from the function

        try: # attempt to send request
            resp = requests.get('https://tempus.xyz/api/search/playersAndMaps/' + query) # only a maximum of 20 players and 5 maps will be returned by the API.

            if resp.status_code == 200: # make sure response 200 OK before parsing json response
                j = json.loads(resp.text) # loads json as python dictionary
                
                if len(j["maps"]) > 5: # the query returned more than 5 results (API already handles this but this is here just in case)
                    print('Too many results. Please enter a more specific query.')
                
                elif len(j["maps"]) == 1: # one exact match was found
                    display_map(j["maps"][0]["name"])

                elif len(j["maps"]) == 0: # no maps containing the string was found
                    print('No maps with a matching name was found.')
                    
                else: # 2-5 results were found
                    choose_one_map(j["maps"]) # pass dict of maps to function to handle multiple results

            else: # there is some sort of http error
                print(resp.status_code + ' error') # output the error code

        except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
            raise SystemExit(e)

        query = input('Search for a map (!q to go back): ').lower() # need to put scanner again here to prompt user input

def main(argv): # takes array of options and arguments. Main is at the bottom because like in c, functions need to be defined above where they are used
    print('tempus.py\n 1. Query users\n 2. Query maps') # list choices
    choice = input('Enter the number next to the feature you want to access (!q to quit): ') # scanner to read input
        
    while choice != '!q':
        if choice == '1': # call user query function
            print('search player')
        elif choice == '2': # call map query function
            search_map()
        else: # display error msg
            print('Invalid input, please enter one of the displayed numbers.')

        print('tempus.py\n 1. Query users\n 2. Query maps') # re-list choices for while loop
        choice = input('Enter the number next to the feature you want to access (!q to quit): ')

    sys.exit() # if user quits at feature menu the program terminates

if __name__ == '__main__': # only run main function if this file is not ran as a module
    main(sys.argv[1:]) # pass all arguments except for the first (the filename itself)
