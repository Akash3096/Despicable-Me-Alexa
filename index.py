import urllib2
import json

API_BASE="http://despicableme.wikia.com/api/v1/Articles/AsSimpleJson?id="


def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.7ad73953-0c37-41da-b66a-334fcb0da850"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."


def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetDescription":
        return get_Character(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print "Ending session."

def handle_session_end_request():
    card_title = "Despicable Me - Thank You"
    speech_output = "Thank you for using the Despicable Me skill. See you next time!"
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Despicable Me Characters"
    speech_output = "Welcome to the Alexa Despicable Me Characters skill. " \
                    "You can ask me for Characters description from Despicable Me movies"
    reprompt_text = "Please ask me for a Character in Despicable Me movie" \
                    "for example Agnes Gru."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


def get_Character(intent):
    session_attributes = {}
    card_title = "Description"
    speech_output = "I'm not sure what character you are specifying" \
                    "Please try again."
    reprompt_text = "I'm not sure which character you are specifying" \
                    "Try asking about Agnes Gru for example."
    should_end_session = False

    if "Characters" in intent["slots"]:
        character = intent["slots"]["Characters"]["value"]
        characterId = (character.lower())
        if (characterId != "unkn"):
            card_title = "Character " + character.title()
            response = urllib2.urlopen(API_BASE + characterId)
            jsonData = json.load(response)
            alexaresponse = jsonData["sections"][0]["content"][0]["text"]

            speech_output = "Description about" + character + " is as follows: "
            reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_character_id(character):
    return {
        "gru": "2033",
    }.get(character, "unkn")


