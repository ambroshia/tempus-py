import sys
import json
import requests
import time

def display_player(playerid): # takes tempus user id as param
    try: # attempt to send request
        resp = requests.get('https://tempus.xyz/api/players/id/' + str(playerid) + '/stats') # query user details

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            p = json.loads(resp.text) # loads json as python dictionary
            print() # newline for formatting

            # print name and country
            print(p["player_info"]["name"]) 
            print('Country: ' + p["player_info"]["country"])

            # print rank info (format points to int to remove floating zero returned by API)
            print('Rank ' + str(p["class_rank_info"]["3"]["rank"]) + ' Soldier (' + str(int(p["class_rank_info"]["3"]["points"])) + ' points)') # solly rank
            print('Rank ' + str(p["class_rank_info"]["4"]["rank"]) + ' Demoman (' + str(int(p["class_rank_info"]["4"]["points"])) + ' points)') # demo rank
            print('Rank ' + str(p["rank_info"]["rank"]) + ' Overall (' + str(int(p["rank_info"]["points"])) + ' points)') # overall rank

            print() # newline for formatting

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)

def choose_one_player(players): # takes dictionary of 2-20 players returned from query
    print(str(len(players)) + ' partial matches found:')

    for i in range(0, len(players)): # range() is used because the index number needs to be printed
        print(' ' + str(i+1) + '. ' + players[i]["name"])

    index = input('Enter the number next to the player you wish to view (!q to go back): ')

    while index != '!q': # !q is the string that allows user to exit from the function

        if index in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']: # first make sure user inputted string that is a number between 1-20
            if int(index) <= len(players): # since the prior statement ensures the input is an int between 1-20, the only other check is to make sure the index is not larger than the player query results
                return players[int(index)-1]["id"] # the player info can be safely returned to player search function
            else: # the inputted index does not exist in the player result dictionary
                print('Invalid input, please enter one of the displayed numbers.')
        else: # user input is not an integer between 1-20
            print('Invalid input, please enter one of the displayed numbers.')
        
        index = input('Enter the number next to the player you wish to view (!q to go back): ') # reprint the input query for the loop

def query_player(query): # API interaction part of player query userflow
    try: # attempt to send request
        resp = requests.get('https://tempus.xyz/api/search/playersAndMaps/' + query) # only a maximum of 20 players and 5 maps will be returned by the API.

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            j = json.loads(resp.text) # loads json as python dictionary
                
            if len(j["players"]) > 20: # the query returned more than 20 results (API already handles this but this is here just in case)
                print('Too many results. Please enter a more specific query.')
                return None
                
            elif len(j["players"]) == 1: # one exact match was found
                return j["players"][0]["id"]

            elif len(j["players"]) == 0: # no players with name containing the string was found
                print('No players with a matching name was found.')
                return None
                    
            else: # 2-20 results were found
                return choose_one_player(j["players"]) # pass dict of players to function to handle multiple results, the final chosen player object is returned to player search function

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code
            return None

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e) # program is exited

def search_player(arg): # User / UI interaction part of player query userflow
    if arg != None: # don't prompt for user input if argument is passed (when program is launched from CLI with args)
        query = arg
    else: # prompt for user input
        query = input('Search for a player (!q to go back): ').lower() # scanner to read input, convert to lower case

    while query != '!q': # !q is the string that allows user to exit from the function

        result = query_player(query) # Send the query string to API interaction function

        if result != None: # API interaction functions will print out error and return None object if any errors occur
            display_player(result) # The result will be a valid tempus ID in the case the player was queried successfully, so it can be passed to the the player display function.

        if arg != None: # If query called at launch with arguments, program should terminate after returning result and not ask input again
            break
        query = input('Search for a player (!q to go back): ').lower() # need to put scanner again here to prompt user input

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
            print('============') # divider for formatting

            # print world records info
            print('World Records:')
            if len(m["soldier_runs"]) > 0: # if the map has been completed on solly, the array will not be empty
                print('Solly: ' + time.strftime('%H:%M:%S', time.gmtime(m["soldier_runs"][0]["duration"])) + ' (' + m["soldier_runs"][0]["name"] +')') # uses python time library, specifically strftime function (originally from c) to convert seconds into hh:mm:ss format
            else: # no one has completed the map as solly, or the map is T0 for solly
                print('Solly: N/A')
            if len(m["demoman_runs"]) > 0: # if the map has been completed on demo, the array will not be empty
                print('Demo: ' + time.strftime('%H:%M:%S', time.gmtime(m["demoman_runs"][0]["duration"])) + ' (' + m["demoman_runs"][0]["name"] +')') # uses python time library, specifically strftime function (originally from c) to convert seconds into hh:mm:ss format
            else: # no one has completed the map as demo, or the map is T0 for demo
                print('Solly: N/A')

            print() # newline for formatting

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)

def choose_one_map(maps): # takes dictionary of 2-5 maps returned from query
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

def query_map(query): # API interaction part of map query userflow
    return None
    
def search_map(arg): # User / UI interaction part of map query userflow
    if arg != None: # don't prompt for user input if argument is passed (when program is launched from CLI with args)
        query = arg
    else: # prompt for user input
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
            raise SystemExit(e) # program is exited

        if arg != None: # If query called at launch with arguments, program should terminate after returning result and not ask input again
            break
        query = input('Search for a map (!q to go back): ').lower() # need to put scanner again here to prompt user input

def search_time(map, player): # look up a player's time for a particular map
    return None

def main(argv): # takes array of options and arguments. Main is at the bottom because like in c, functions need to be defined above where they are used
    if len(argv) > 0: # if the program was launched with arguments don't prompt user input
        if argv[0].lower() == '-h' or argv[0].lower() == '--help':
            print('help')
        elif argv[0].lower() == '-m' or argv[0].lower() == '--map':
            search_map(argv[1].lower())
        elif argv[0].lower() == '-p' or argv[0].lower() == '--player':
            search_player(' '.join(argv[1:]).lower()) # join player name arguments (for player names that contain spaces)
        else:
            print('Unknown argument.')
            print('help')

    else: # run the program as normal if no arguments
        print('tempus.py - lookup users and maps\n 1. Query users\n 2. Query maps') # list choices
        choice = input('Enter the number next to the feature you want to access (!q to quit): ') # scanner to read input
            
        while choice != '!q':
            if choice == '1': # call user query function
                search_player(None) # need to pass an arg, so pass None
            elif choice == '2': # call map query function
                search_map(None) # need to pass an arg, so pass None
            else: # display error msg
                print('Invalid input, please enter one of the displayed numbers.')

            print('tempus.py - lookup users and maps\n 1. Query users\n 2. Query maps') # re-list choices for while loop
            choice = input('Enter the number next to the feature you want to access (!q to quit): ')

    sys.exit() # if user quits at feature menu the program terminates

if __name__ == '__main__': # only run main function if this file is not ran as a module
    main(sys.argv[1:]) # pass all arguments except for the first (the filename itself)
