from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import json
from .eliza import Eliza
from pprint import pprint
import requests
from filestack import Client

client = Client("Ax6UCGIqiRRKyjRjHAYEwz")

eliza = Eliza()
eliza.load('./webhook/doctor.txt')

def convertToSpeech(input_text, id):
    language = 'en'
    myobj = gTTS(text = input_text, lang=language, slow=False)
    myobj.save("./{}.mp3".format(id))
    newurl = client.upload(filepath="./{}.mp3".format(id))
    return newurl.url


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
        headers = {
                    'Authorization': 'Bearer 665ab736-26d3-4d7d-ba98-879a2e37db8e',
                    'Content-Type': 'application/json'
                }
        pprint(data_sent)
        if "contacts" in data_sent:
            url = "https://app.kwiqreply.io/api/messages"
            try:
                msg = data_sent["messages"][0]["text"]["body"].lower()
            except KeyError:
                msg = data_sent["messages"][0]["interactive"]["list_reply"]['title'].lower()
            msg_to = data_sent["contacts"][0]["wa_id"]
            if msg == "menu":
                payload = json.dumps({
                "to": msg_to,
                "recipient_type": "individual",
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "header": {
                    "type": "text",
                    "text": "Sample menu"
                    },
                    "body": {
                    "text": "Choose what you want"
                    },
                    "footer": {
                    "text": "Powered by KwiqReply"
                    },
                    "action": {
                    "button": "Choose",
                    "sections": [
                        {
                        "title": "Image",
                        "rows": [
                            {
                            "id": "image",
                            "title": "image",
                            "description": ""
                            },
                            {
                            "id": "audio",
                            "title": "audio",
                            "description": ""
                            },
                            {
                            "id": "video",
                            "title": "video",
                            "description": ""
                            },
                            {
                            "id": "document",
                            "title": "document",
                            "description": ""
                            },
                            {
                            "id": "buttons",
                            "title": "buttons",
                            "description": ""
                            },
                            {
                            "id": "address",
                            "title": "address",
                            "description": ""
                            },
                            {
                            "id": "contact",
                            "title": "contact",
                            "description": ""
                            }
                        ]
                        }
                    ]
                    }
                }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                return HttpResponse("Image Sent!")
            elif msg in ["image", "audio", "video", "document"]:
                payload_dict = {
                    "to": msg_to,
                    "type": msg,
                    "recipient_type": "individual",
                    msg: {
                        "link": "https://github.com/jaynammodi/sample_content/blob/master/image.jpg?raw=true",
                        "caption": "Sample Image"
                    } if msg == "image" else {
                        "link": "https://github.com/jaynammodi/sample_content/blob/master/audio.mp3?raw=true",
                    } if msg == "audio" else {
                        "link": "https://github.com/jaynammodi/sample_content/blob/master/video.mp3?raw=true",
                        "caption": "Sample Video"
                    } if msg == "video" else {
                        "link": "https://github.com/jaynammodi/sample_content/blob/master/text.txt?raw=true",
                        "caption": "Sample Document",
                        "filename": "text.txt"
                    }
                }
                payload = json.dumps(payload_dict)

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                return HttpResponse("Image Sent!")
            elif msg == "buttons":
                payload = json.dumps({
                "to": msg_to,
                "recipient_type": "individual",
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "header": {
                    "type": "text",
                    "text": "Sample Buttons"
                    },
                    "body": {
                    "text": "Whatever body"
                    },
                    "footer": {
                    "text": "Kwiqreply"
                    },
                    "action": {
                    "buttons": [
                        {
                        "type": "reply",
                        "reply": {
                            "id": "menu",
                            "title": "menu"
                        }
                        },
                        {
                        "type": "reply",
                        "reply": {
                            "id": "eliza",
                            "title": "hi eliza"
                        }
                        },
                        {
                        "type": "reply",
                        "reply": {
                            "id": "eliza_terminate",
                            "title": "bye eliza"
                        }
                        }
                    ]
                    }
                }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                return HttpResponse("Webhook received!")
            elif msg == "address":
                payload = json.dumps({
                "to": msg_to,
                "type": "location",
                "recipient_type": "individual",
                "location": {
                    "longitude": "27.2046",
                    "latitude": "77.4977",
                    "name": "KwiqReply",
                    "address": "Faith Centre"
                }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                return HttpResponse("Webhook received!")
            elif msg == "contact":
                payload = json.dumps({
                "to": msg_to,
                "type": "contacts",
                "recipient_type": "individual",
                "contacts": [
                    {
                    "addresses": [
                        {
                        }
                    ],
                    "birthday": "",
                    "emails": [
                        {
                        }
                    ],
                    "ims": [],
                    "name": {
                        "first_name": "Jaynam",
                        "formatted_name": "Jaynam Modi",
                        "last_name": "Modi"
                    },
                    "org": {
                    },
                    "phones": [
                        {
                        "phone": "+917990326788",
                        "type": "Mobile"
                        }
                    ],
                    "urls": []
                    }
                ]
                })

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                return HttpResponse("Webhook received!")
            else:
                payload = json.dumps({
                "to": msg_to,
                "type": "text",
                "text": {
                    "body": eliza.generateResponse(msg)
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

            # payload = json.dumps({
            #     "to": data_sent["contacts"][0]["wa_id"],
            #     "type": "text",
            #     "text": {
            #         "body": eliza.generateResponse(data_sent["messages"][0]["text"]["body"])
            #     }
            # })

        return HttpResponse("Webhook received!")
    elif request.method == 'GET':
        print(" > Get request received")
        return HttpResponse("Webhook received!")