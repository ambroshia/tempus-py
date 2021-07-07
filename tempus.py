import sys
import json
import requests

def display_map(mapname): # takes the full map name as a string parameter
    try: # attempt to send request
        resp = requests.get('https://tempus.xyz/api/maps/name/' + mapname + '/fullOverview') # query map overview info

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            map = json.loads(resp.text) # loads json as python dictionary

            # print map name
            print(map["map_info"]["name"] + ' by ', end='') # end='' parameter to make print function not end with newline.
            
            # print map authors differently depending on how many of them there are
            if len(map["authors"]) == 1: # only one author; just print it
                print(map["authors"][0]["name"])

            elif len(map["authors"]) == 2: # print two authors joined by and
                print(map["authors"][0]["name"] + ' and ' + map["authors"][1]["name"])

            else: # for three or more, join all the authors with commar except for the last, joined by and
                numauthors = len(map["authors"]) # store number of authors in a variable

                for i in range(0, numauthors - 2): # for loop will iterate through all authors except the last 2
                    print(map["authors"][i]["name"] + ', ', end='') # end='' parameter to make print function not end with newline.
                
                print(map["authors"][numauthors-2]["name"]+' and '+map["authors"][numauthors-1]["name"]) # print the last two authors joined by 'and'
            
            # print tier info
            print('Solly T'+str(map["tier_info"]["soldier"])+' | Demo T'+str(map["tier_info"]["demoman"]))
                

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)

def main(argv): # takes array of options and arguments
    query = input('Search for a map: ') # scanner to read input

    try: # attempt to send request
        resp = requests.get('https://tempus.xyz/api/search/playersAndMaps/' + query) # only a maximum of 20 players and 5 maps will be returned by the API.

        if resp.status_code == 200: # make sure response 200 OK before parsing json response
            j = json.loads(resp.text) # loads json as python dictionary
            
            if len(j["maps"]) > 5: # the query returned more than 5 results (API already handles this but this is here just in case)
                print('Too many results. Please enter a more specific query.')
            
            elif len(j["maps"]) == 1: # one exact match was found
                display_map(j["maps"][0]["name"])
                
            else: # 2-5 results were found
                print('TEST')

        else: # there is some sort of http error
            print(resp.status_code + ' error') # output the error code

    except requests.exceptions.RequestException as e:  # all request errors inherit from RequestException
        raise SystemExit(e)



if __name__ == "__main__":
    main(sys.argv[1:]) # pass all arguments except for the first (the filename itself)
