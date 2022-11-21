from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
# from gtts import gTTS
import json
from pprint import pprint
import requests
import openai

flag = 0
user_details = {
    "name": "",
    "num": "",
    "email": ""
}

openai.api_key = "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"

images = {
    "img001": "https://assets.myntassets.com/dpr_1.5,q_60,w_400,c_limit,fl_progressive/assets/images/18458460/2022/5/28/c28d223f-6a82-46be-8922-6a21172bd2841653714541319AfroJackWomenWhiteSneakers1.jpg",
    "img002": "https://cdn-fnknc.nitrocdn.com/jwqHRGAzpUgGskUSHlppNQzwuXgXIKwg/assets/static/optimized/rev-2f126d7/wp-content/uploads/2022/02/CommonProjects_BestBlackSneakers--675x333.jpg",
    "img003": "https://m.media-amazon.com/images/I/81st5nBcnnL._UY695_.jpg",
    
}

headers = {'Authorization': 'Bearer 665ab736-26d3-4d7d-ba98-879a2e37db8e', 'Content-Type': 'application/json'}
url = "https://app.kwiqreply.io/api/messages"
target_number = "917990326788"


conversation_history = """
Daisy is an AI assistant that works as a salesperson for an apparel store. She has access to the store's inventory and can help you find the right product for you. It's intelligence is limited to the store's inventory and cannot answer any questions beyond its scope . Here's a conversation with {}, pretend to be daisy:
"""

def usrMsg(msg):
    global conversation_history, user_details
    conversation_history = conversation_history + "\n" + user_details["name"] + ": " + msg + "\nDaisy: "

def botMsg(msg):
    global conversation_history, user_details
    conversation_history = conversation_history + "\nDaisy: " + msg

def startConversation():
    global headers, url, target_number, user_details, flag
    botMsg("Welcome to Flipkart, I am Daisy, May I please know your name?")
    payload = json.dumps({
        "to": user_details["num"],
        "type": "image",
        "recipient_type": "individual",
        "image": {
            "link": "https://storiesflistgv2.blob.core.windows.net/stories/2019/03/article_banner_press_release_26_03_19_v1-01.jpg",
            "caption": "Welcome to Flipkart, I am Daisy, May I please know your name?"
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    flag += 1
    print(response.text)

def sendBrochure():
    global headers, url, target_number, user_details, flag, conversation_history
    payload = json.dumps({
        "to": user_details["num"],
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
            "type": "text",
            "text": "Shopping Menu - Sample"
            },
            "body": {
            "text": "Hi {}, welcome to our store, please choose a product you want to know more about:".format(user_details['name'])
            },
            "footer": {
            "text": "Click on view products to see!"
            },
            "action": {
            "button": "View Products",
            "sections": [
                {
                "title": "Clothes",
                "rows": [
                    {
                    "id": "white_t",
                    "title": "White T-Shirt",
                    "description": "Solid white Polycot T-Shirt"
                    },
                    {
                    "id": "black_t",
                    "title": "Black T-Shirt",
                    "description": "Solid black Polycot T-Shirt"
                    },
                ]
                },
                {
                "title": "Shoes",
                "rows": [
                    {
                    "id": "white_sneakers",
                    "title": "White Sneakers",
                    "description": "Contemporary Classic White Sneakers"
                    },
                    {
                    "id": "black_sneakers",
                    "title": "Black Sneakers",
                    "description": "Contemporary Classic Black Sneakers"
                    },
                ]
                }
            ]
            }
        }
    })
    print(" > Generated Payload: ", payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(conversation_history)




def setName(name):
    global user_details, conversation_history, flag
    user_details["name"] = name
    conversation_history.format(name)
    usrMsg(name)
    flag += 1
    sendBrochure()

def generatePrompt(userInput):
    global conversation_history
    conversation_history = conversation_history + userInput.strip() + "\nDaisy: "
    return conversation_history

def generateResponse(userInput):
    global conversation_history
    thisPrompt = generatePrompt(userInput)
    response = openai.Completion.create(
        model="text-davinci-002",
        max_tokens=4097 - len(thisPrompt),
        prompt=thisPrompt,
        temperature=0.6
    )
    reply = response["choices"][0]["text"].strip()
    conversation_history = conversation_history + reply + "\nJaynam: "
    # print(" !> debug:  ", )
    return reply


@csrf_exempt
def webhook(request):
    global flag, form_data, headers, url, target_number, user_details
    
    if request.method == 'POST':

        data_sent = json.loads(request.body)

        print(" > Data received from Webhook is: ")
        pprint(data_sent)
        
        if "contacts" in data_sent:
            try:
                data_type = data_sent["messages"][0]["interactive"]["type"]
            except KeyError:
                data_type = "text"
            try:
                msg = data_sent["messages"][0]["text"]["body"].lower()
            except KeyError:
                msg = data_sent["messages"][0]["interactive"][data_type]["id"].lower()

            msg_to = data_sent["contacts"][0]["wa_id"]

            user_details["num"] = msg_to

            if msg_to != target_number and target_number != "":
                return HttpResponse(" > Not your number")

            if flag == 1:
                print(" > Setting Name")
                setName(msg)
            elif flag > 1:
                print(" > Sending Brochure")
                sendBrochure()

            elif "shopdemo" in msg:
                startConversation()

            # if "shopflow" in msg:
            #     # payload = json.dumps({
            #     # "to": msg_to,
            #     # "recipient_type": "individual",
            #     # "type": "interactive",
            #     # "interactive": {
            #     #     "type": "list",
            #     #     "header": {
            #     #     "type": "text",
            #     #     "text": "Hi, I'm Daisy. I'm here to help you find the right pair of sneakers for you. What are you looking for?",
            #     #     },
            #     #     "body": {
            #     #     "text": "Find a pair of sneakers",
            #     #     },
            #     #     "footer": {
            #     #     "text": "Select from the menu below",
            #     #     },
            #     #     "action": {
            #     #     "button": "Send",
            #     #     "sections": [
            #     #         {
            #     #         "title": "Shoes",
            #     #         "rows": [
            #     #             {
            #     #             "id": "msneakers",
            #     #             "title": "Sneakers for Men",
            #     #             "description": "whatever"
            #     #             },
            #     #             {
            #     #             "id": "fsneakers",
            #     #             "title": "Sneakers for women",
            #     #             "description": "whatever2"
            #     #             },
            #     #             {
            #     #             "id": "usneakers",
            #     #             "title": "Unisex Sneakers",
            #     #             "description": "whatever3"
            #     #             },
            #     #         ]
            #     #         },
            #     #     ]  
            #     #     }
            #     # }
            #     # }
            #     # )


            #     payload = json.dumps({
            #         "to": msg_to,
            #         "recipient_type": "individual",
            #         "type": "interactive",
            #         "interactive": {
            #             "type": "list",
            #             "header": {
            #             "type": "text",
            #             "text": "Shopping Menu - Sample"
            #             },
            #             "body": {
            #             "text": "Choose a product from the variety mentioned"
            #             },
            #             "footer": {
            #             "text": "Click on view products to see!"
            #             },
            #             "action": {
            #             "button": "View Products",
            #             "sections": [
            #                 {
            #                 "title": "Clothes",
            #                 "rows": [
            #                     {
            #                     "id": "white_t",
            #                     "title": "White T-Shirt",
            #                     "description": "Solid white Polycot T-Shirt"
            #                     },
            #                     {
            #                     "id": "black_t",
            #                     "title": "Black T-Shirt",
            #                     "description": "Solid black Polycot T-Shirt"
            #                     },
            #                 ]
            #                 },
            #                 {
            #                 "title": "Shoes",
            #                 "rows": [
            #                     {
            #                     "id": "white_sneakers",
            #                     "title": "White Sneakers",
            #                     "description": "Contemporary Classic White Sneakers"
            #                     },
            #                     {
            #                     "id": "black_sneakers",
            #                     "title": "Black Sneakers",
            #                     "description": "Contemporary Classic Black Sneakers"
            #                     },
            #                 ]
            #                 }
            #             ]
            #             }
            #         }
            #     })

            #     response = requests.request("POST", url, headers=headers, data=payload)

            #     print(response.text)

            elif msg != "":
                raw_msg = generateResponse(msg)
                print(" > Generated Response: ", raw_msg)
                # if "ImageID" in raw_msg:
                #     clean_txt, imgID = raw_msg.split("[ImageID=")
                #     imgID = imgID[:-1]
                #     print(clean_txt, imgID)
                #     payload = json.dumps({
                #         "to": msg_to,
                #         "type": "image",
                #         "recipient_type": "individual",
                #         "image": {
                #             "link": images[imgID],
                #             "caption": clean_txt
                #         }
                #     })
                payload = json.dumps({
                    "to": msg_to,
                    "type": "text",
                    "text": {
                        "body": raw_msg
                    }
                })
                print(" > Generated Payload: ", payload)
                response = requests.request("POST", url, headers=headers, data=payload)
                print(" > else - AI : ", response.json())
        return HttpResponse("Webhook received!")
    elif request.method == 'GET':
        print(" > Get request received")
        return HttpResponse("Webhook received!")