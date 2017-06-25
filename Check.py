import urllib2
import json
import requests

API_BASE="http://despicableme.wikia.com/api/v1/Articles/AsSimpleJson?id="



def get_Character():
    character = "Gru"
    characterId = get_character_id(character.lower())
    print "Got the character ID"
    response = requests.get(API_BASE + characterId)
    #jsonData = response.json()
    jsonData = json.loads(response)

    print "Got the response"
    alexaresponse = jsonData["sections"][0]["content"][0]["text"]
    print "Got the content"




def get_character_id(character):
    return {
        "gru": "2033",
    }.get(character, "unkn")


get_Character()