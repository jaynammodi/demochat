from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import json
from .eliza import Eliza
from pprint import pprint
import requests

eliza = Eliza()
eliza.load('./webhook/doctor.txt')

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
        print(" > Data received from Webhook is: ")
        # pprint(request.body)
        data_sent = json.loads(request.body)
        pprint(data_sent)

        url = "https://app.kwiqreply.io/api/messages"

        payload = json.dumps({
            "to": data_sent["contacts"][0]["wa_id"],
            "type": "text",
            "text": {
                "body": eliza.generateResponse(data_sent["messages"][0]["text"]["body"])
            }
        })
        headers = {
            'Authorization': 'Bearer 665ab736-26d3-4d7d-ba98-879a2e37db8e',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        return HttpResponse("Webhook received!")
    elif request.method == 'GET':
        print(" > Get request received")
        return HttpResponse("Webhook received!")