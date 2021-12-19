import sys
import json
import requests
import time

def choose_one_player(players): # takes dictionary of 2-20 players returned from query. Returns a valid player ID.
    print(str(len(players)) + ' partial matches found:')

    for i in range(0, len(players)): # range() is used because the index number needs to be printed
        print(' ' + str(i+1) + '. ' + players[i]["name"])

    index = input('Enter the number next to the player you wish to view (!q to go back): ')

    while index != '!q': # !q is the string that allows user to exit from the function

        if index in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']: # first make sure user inputted string that is a number between 1-20
            if int(index) <= len(players): # since the prior statement ensures the input is an int between 1-20, the only other check is to make sure the index is not larger than the player query results
                return players[int(index)-1] # the player object can be safely returned to player search function
            else: # the inputted index does not exist in the player result dictionary
                print('Invalid input, please enter one of the displayed numbers.')
        else: # user input is not an integer between 1-20
            print('Invalid input, please enter one of the displayed numbers.')
        
        index = input('Enter the number next to the player you wish to view (!q to go back): ') # reprint the input query for the loop

def choose_one_map(maps): # takes dictionary of 2-5 maps returned from query. Returns a valid full map name.
    print(str(len(maps)) + ' partial matches found:')

    for i in range(0, len(maps)): # range() is used because the index number needs to be printed
        print(' ' + str(i+1) + '. ' + maps[i]["name"])

    index = input('Enter the number next to the map you wish to view (!q to go back): ')

    while index != '!q': # !q is the string that allows user to exit from the function

        if index in ['1','2','3','4','5']: # first make sure user inputted string that is a number between 1-5
            if int(index) <= len(maps): # since the prior statement ensures the input is an int between 1-5, the only other check is to make sure the index is not larger than the map query results
                return maps[int(index)-1]["name"] # the full map name can be safely returned to map search function
                break # after map info is displayed, return to search map function
            else: # the inputted index does not exist in the map result dictionary
                print('Invalid input, please enter one of the displayed numbers.')
        else: # user input is not an integer between 1-5
            print('Invalid input, please enter one of the displayed numbers.')
        
        index = input('Enter the number next to the map you wish to view (!q to go back): ') # reprint the input query for the loop

def query_player(query): # API interaction part of player query userflow. When successful, returns a valid player object.
    try: # attempt to send request
        resp = requests.get('https://tempus.xyz/api/search/playersAndMaps/' + query) # only a maximum of 20 players and 5 maps will be returned by the API.

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            j = json.loads(resp.text) # loads json as python dictionary
                
            if len(j["players"]) > 20: # the query returned more than 20 results (API already handles this but this is here just in case)
                print('Too many results. Please enter a more specific query.')
                return None
                
            elif len(j["players"]) == 1: # one exact match was found
                return j["players"][0] # returns player object, including ID, name, and steamID

            elif len(j["players"]) == 0: # no players with name containing the string was found
                print('No players with a matching name was found.')
                return None
                    
            else: # 2-20 results were found
                return choose_one_player(j["players"]) # pass dict of players to function to handle multiple results, the final chosen player's id is returned to player search function

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code
            return None

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e) # program is exited

def query_map(query): # API interaction part of map query userflow. When successful, returns a valid full map name.
    try: # attempt to send request
        resp = requests.get('https://tempus.xyz/api/search/playersAndMaps/' + query) # only a maximum of 20 players and 5 maps will be returned by the API.

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            j = json.loads(resp.text) # loads json as python dictionary
                
            if len(j["maps"]) > 5: # the query returned more than 5 results (API already handles this but this is here just in case)
                print('Too many results. Please enter a more specific query.')
                return None
                
            elif len(j["maps"]) == 1: # one exact match was found
                return j["maps"][0]["name"] 

            elif len(j["maps"]) == 0: # no maps containing the string was found
                print('No maps with a matching name was found.')
                return None
                    
            else: # 2-5 results were found
                return choose_one_map(j["maps"]) # pass dict of maps to function to handle multiple results, the final chosen map name is returned to map search function

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code
            return None

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e) # program is exited

def query_soldier_time(playerid, mapname): # API interaction part of userflow to look up a player's soldier time for a map. When successful, returns dict object containing a player's soldier time for a map.
    try: # attempt to send request
        # original url: https://tempus.xyz/api/maps/name/${map}/zones/typeindex/${zoneType}/${zoneIndex}/records/player/${player.id}/${classIndex}
        resp = requests.get('https://tempus.xyz/api/maps/name/' + mapname + '/zones/typeindex/map/1/records/player/' + str(playerid) + '/3') # classIndex 3 is soldier

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            r = json.loads(resp.text) # loads json as python dictionary

            if r["result"] != None: # The result section is not empty (The player has completed the map at least once as soldier)
                return r # returns the entire dictionary containing the run and map run info
            else: # The result section is empty (The player has not completed the map)
                return None

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code
            return None
        
    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)

def query_demo_time(playerid, mapname): # API interaction part of userflow to look up a player's demoman time for a map. When successful, returns dict object containing a player's demoman time for a map.
    try: # attempt to send request
        # original url: https://tempus.xyz/api/maps/name/${map}/zones/typeindex/${zoneType}/${zoneIndex}/records/player/${player.id}/${classIndex}
        resp = requests.get('https://tempus.xyz/api/maps/name/' + mapname + '/zones/typeindex/map/1/records/player/' + str(playerid) + '/4') # classIndex 4 is demoman

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            r = json.loads(resp.text) # loads json as python dictionary

            if r["result"] != None: # The result section is not empty (The player has completed the map at least once as soldier)
                return r # returns the entire dictionary containing the run and map run info
            else: # The result section is empty (The player has not completed the map)
                return None

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code
            return None
        
    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)

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
                print('Soldier: ' + time.strftime('%H:%M:%S', time.gmtime(m["soldier_runs"][0]["duration"])) + ' (' + m["soldier_runs"][0]["name"] +')') # uses python time library, specifically strftime function (originally from c) to convert seconds into hh:mm:ss format
            else: # no one has completed the map as solly, or the map is T0 for solly
                print('Soldier: N/A')
            if len(m["demoman_runs"]) > 0: # if the map has been completed on demo, the array will not be empty
                print('Demoman: ' + time.strftime('%H:%M:%S', time.gmtime(m["demoman_runs"][0]["duration"])) + ' (' + m["demoman_runs"][0]["name"] +')') # uses python time library, specifically strftime function (originally from c) to convert seconds into hh:mm:ss format
            else: # no one has completed the map as demo, or the map is T0 for demo
                print('Demoman: N/A')

            print() # newline for formatting

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)

def search_time(player, mapname, state): # User / UI interaction part of userflow to look up a player's times for a map.
    while True: # The function will continually look up map runs until the exit signal !q is inputted in one of the subqueries below.

        if player == None: # player info was not passed, need to ask user to input player
            while True: # infinite loop, as the function is designed to continually prompt the user to query a player, until a player is found, or until the function is exited via !q
                query = input('Search for the player whose records you wish to find (!q to go back): ').lower()

                if (query == '!q'):
                    return # this will exit the search_time function instantly

                player = query_player(query) # pass user inputted string into player query function

                if player != None: # break from the infinite loop after a player has been found (the player value is filled)
                    break

        if mapname == None: # map name was not passed, need to ask user to input map name
            while True: # infinite loop, as the function is designed to continually prompt the user to query a map, until a map is found, or until the function is exited via !q
                query = input('Search for map runs by ' + player["name"] + ' (!q to go back): ').lower()

                if (query == '!q'):
                    return # this will exit the search_time function instantly

                mapname = query_map(query) # pass user inputted string into map query function

                if mapname != None: # break from the infinite loop after a map has been found (the map value is filled)
                    break

        print() # newline for formatting
        sollytime = query_soldier_time(player["id"], mapname) # pass player id and map name into API function to fetch run info
        if sollytime != None: # a soldier record on the map was found
            print('Soldier: ' + player["name"] + ' is ranked ' + str(sollytime["result"]["rank"]) + '/' + str(sollytime["completion_info"]["soldier"]) + ' on ' + mapname + ' with time: ' + time.strftime('%H:%M:%S', time.gmtime(sollytime["result"]["duration"])))
        else:
            print('Soldier: No record found.')

        demotime = query_demo_time(player["id"], mapname)  # pass player id and map name into API function to fetch run info
        if demotime != None: # a demoman record on the map was found
            print('Demoman: ' + player["name"] + ' is ranked ' +  str(demotime["result"]["rank"]) + '/' + str(demotime["completion_info"]["demoman"]) + ' on ' + mapname + ' with time: ' + time.strftime('%H:%M:%S', time.gmtime(demotime["result"]["duration"])))
        else:
            print('Demoman: No record found.')
        print() # newline for formatting

        # state is passed when initialising function, and dictates which value needs to be reset at the end of each loop of the function
        # e.g. if search_time is called from the main menu, or from a player's page, the mapname will need to be reset on each loop to allow the user to query any map runs for the given user
        #      whereas if search_time is called from a map's page, the player will need to be reset on each loop to allow the user to look up runs by different players for the given map
        if state == 0: # mapname needs to be reset - function is called from main menu / player info page
            mapname = None
        else: # player needs to be reset - function is called from map info page
            player = None

def search_player(arg): # User / UI interaction part of player query userflow
    if arg != None: # don't prompt for user input if argument is passed (when program is launched from CLI with args)
        query = arg
    else: # prompt for user input
        query = input('Search for a player (!q to go back): ').lower() # scanner to read input, convert to lower case

    while query != '!q': # !q is the string that allows user to exit from the function

        result = query_player(query) # Send the query string to API interaction function

        if result != None: # API interaction functions will print out error and return None object if any errors occur
            display_player(result["id"]) # The result will be a valid player object in the case the player was queried successfully, so it can be passed to the the player display function.

        if arg != None: # If query called at launch with arguments, program should terminate after returning result and not ask input again
            break
        query = input('Search for a player (!q to go back): ').lower() # need to put scanner again here to prompt user input

def search_map(arg): # User / UI interaction part of map query userflow
    if arg != None: # don't prompt for user input if argument is passed (when program is launched from CLI with args)
        query = arg
    else: # prompt for user input
        query = input('Search for a map (!q to go back): ').lower() # scanner to read input, convert to lower case

    while query != '!q': # !q is the string that allows user to exit from the function

        result = query_map(query) # Send the query string to API interaction function

        if result != None: # API interaction functions will print out error and return None object if any errors occur
            display_map(result) # The result will be a valid full map name in the case the map was queried successfully, so it can be passed to the the map display function.

        if arg != None: # If query called at launch with arguments, program should terminate after returning result and not ask input again
            break
        query = input('Search for a map (!q to go back): ').lower() # need to put scanner again here to prompt user input

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
        print('tempus.py - lookup users and maps\n 1. Query users\n 2. Query maps\n 3. Query map runs') # list choices
        choice = input('Enter the number next to the feature you want to access (!q to quit): ') # scanner to read input
            
        while choice != '!q':
            if choice == '1': # call user query function
                search_player(None) # need to pass an arg, so pass None
            elif choice == '2': # call map query function
                search_map(None) # need to pass an arg, so pass None
            elif choice == '3': # call map query map run times
                search_time(None, None, 0) # args are required, search_time function will automatically ask players to fill in the args if none are provided.
            else: # display error msg
                print('Invalid input, please enter one of the displayed numbers.')

            print('tempus.py - lookup users and maps\n 1. Query users\n 2. Query maps\n 3. Query map runs') # re-list choices for while loop
            choice = input('Enter the number next to the feature you want to access (!q to quit): ')

    sys.exit() # if user quits at feature menu the program terminates

if __name__ == '__main__': # only run main function if this file is not ran as a module
    main(sys.argv[1:]) # pass all arguments except for the first (the filename itself)
