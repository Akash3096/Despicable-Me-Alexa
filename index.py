import urllib2
import json

API_BASE="1"



def get_Character():
    character = "Gru"
    characterId = get_character_id(character.lower())
    print "Got the character ID"




def get_character_id(character):
    return {
        "gru": "2033",
    }.get(character, "unkn")