from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import json

def convertToSpeech(input_text, id):
    language = 'en'
    myobj = gTTS(text = input_text, lang=language, slow=False)
    myobj.save("welcome.mp3")


'''
{"contacts": [{"profile": {"name": "Jaynam Modi"}, "wa_id": "917990326788"}], 
"messages": [{"from": "917990326788", "id": "ABEGkXmQMmeIAhCNtbem7x5-UKxpF_sdPZxj", 
"text": {"body": "hellooo"}, 
"timestamp": "1667998564", "type": "text"}]}'
'''


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        print(" > Data received from Webhook is: ", request.body)
        data_sent = json.loads(request.body)
        payload = {
                "company-name" : "kwiqreply",
                "event-data": {
                    "event-name" : "basic_kwiq_tmp",
                    "event-id": "2817"
                },
                "parameters":{
                    "phone-number":"917990326788",
                    "variables":[data_sent["contacts"][0]['profile']['name'],"KwiqReply"],
                    "url-variable":"url-endpoint",
                    "header" : {
                    #     "link" : "<If it contains media then link of media>",
                    # "filename":"<required if the media type is of document type>"
                    }
                }
            }
        return HttpResponse("Webhook received!")
    elif request.method == 'GET':
        print(" > Get request received")
        return HttpResponse("Webhook received!")