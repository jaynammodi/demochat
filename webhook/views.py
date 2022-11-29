from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
from time import sleep
from pymongo import MongoClient
import json, requests, openai, re, csv

client = MongoClient("mongodb+srv://voldemort:<password>@aicluster.wf8teze.mongodb.net/?retryWrites=true&w=majority")
db = client.test



# DATA PROCESSING
def cleanDB(db):
    db = {k: v for k, v in db.items() if v != ""}
    return db

def parseCSV(filepath):
    with open(filepath, mode='r') as infile:
        mydict = {rows[0]:rows[1] for rows in csv.reader(infile)}
    return mydict
        
def buildProductDB(filepath):
    global product_db
    product_db = cleanDB(parseCSV(filepath))

def buildCustomerDB(filepath):
    global customer_db
    customer_db = cleanDB(parseCSV(filepath))

def buildOrdersDB(filepath):
    global order_db
    order_db = cleanDB(parseCSV(filepath))

def buildOffersDB(filepath):
    global offers_db
    offers_db = cleanDB(parseCSV(filepath))

def buildStoreDetails():
    global store_details
    store_details = {
        "name": "Flipkart",
        "address": "Bengaluru, Karnataka",
        "phone": "080 4666 4666",
        "email": "jaynam@kwiqreply.io",
        "website": "https://www.flipkart.com/"
    }

def buildStoreDBS(dir):
    buildProductDB(dir + "products.csv")
    buildCustomerDB(dir + "customers.csv")
    buildOrdersDB(dir + "orders.csv")
    buildOffersDB(dir + "offers.csv")
    buildStoreDetails()


    



# MAIN CHAT

flag = 0

user_details = {
    "name": "",
    "num": "",
    "email": ""
}

openai.api_key = "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"

order_details = {
     "917990326788": "<TRACKING DETAILS HERE>",
}

images = {
    "t001": "https://m.media-amazon.com/images/I/61QZ72APrOL._UL1000_.jpg",
    "t002": "https://pyxis.nymag.com/v1/imgs/7e2/f1d/2ffe5d192c7d9971f10b4bb99418376fee-Uniqlo-U-black-tshirt.2x.rdeep-vertical.w245.jpg",
    "s001": "https://assets.myntassets.com/dpr_1.5,q_60,w_400,c_limit,fl_progressive/assets/images/10620008/2022/6/2/7a8a978e-09fc-4bb8-b36b-69dedd95a53b1654169026973-The-Roadster-Lifestyle-Co-Men-White-Sneakers-666165416902666-1.jpg",
    "s002": "https://media1.popsugar-assets.com/files/thumbor/KllFvR01AcxP4DyOl7Q7wlWnvuM/0x422:1536x1958/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2021/08/03/730/n/1922564/abdeee7061096f645917d1.36444286_/i/Cute-Black-Sneakers.jpg",
}

sample_url = "https://api.openai.com/v1/engines/davinci/completions"

urls = {
    "t001": sample_url,
    "t002": sample_url,
    "s001": sample_url,
    "s002": sample_url
}

headers = {'Authorization': 'Bearer 665ab736-26d3-4d7d-ba98-879a2e37db8e', 'Content-Type': 'application/json'}

url = "https://app.kwiqreply.io/api/messages"

target_numbers = ["917990326788"]


conversation_history = """
! Daisy is an AI assistant that works as a salesperson for an apparel store. She has access to the store's inventory and can help you find the right product for you. It's intelligence is limited to the store's inventory and cannot answer any questions beyond its scope.
! Store Inventory:
! -------BEGIN STORE INVENTORY-------
! - White T-Shirt - White Polycot TShirt - 1000 INR - 10 in stock - Sizes: S, M, L, XL - PRODUCT_ID: t001"
! - Black T-Shirt - Black Polycot TShirt - 1000 INR - 10 in stock - Sizes: S, M, L, XL - PRODUCT_ID: t002"
! - White Sneakers - White Sneakers - 2000 INR - 10 in stock - Sizes: 6, 7, 8, 9, 10 - PRODUCT_ID: s001"
! - Black Sneakers - Black Sneakers - 2000 INR - 10 in stock - Sizes: 6, 7, 8, 9, 10 - PRODUCT_ID: s002"
! -------END STORE INVENTORY-------

! When the user finalises a product, Daisy will send the user a link to the product page on the store's website.
! When the user is interested in a product, Daisy will send the user the Image and the Store URL of the product using the keyword "[**INSERT_PRODUCT=PRODUCT_ID**]". Example ->
! > User: white sneakers
! > Daisy: The white sneakers cost 2000 INR and are available in sizes 6, 7, 8, 9, 10. Here's the store Page: [**INSERT_PRODUCT=s001**]

! When the user wants to see any product, Daisy will send the user the catalog with the keyword "[**INSERT_CATALOG_HERE**]". Example ->
! > User: more products
! > Daisy: [**INSERT_CATALOG_HERE**]

! If the user wants to track their order, Daisy will send the user the tracking link with the keyword "[**INSERT_TRACKING_LINK_HERE**]". Example ->
! > User: track my order
! > Daisy: [**INSERT_TRACKING_LINK_HERE**]

! If the user wants help with their order, regarding cancellation, refunds, exchanges or any other issue, Daisy will send the user the keyword "[**CONNECT_TO_AGENT**]". Example ->
! > User: I want to cancel my order
! > Daisy: [**CONNECT_TO_AGENT**]

! If the user wants to know the store's contact details, Daisy will send the user the keyword "[**INSERT_CONTACT_DETAILS**]". Example ->
! > User: I want to know your contact details
! > Daisy: [**INSERT_CONTACT_DETAILS**]

! Here's a conversation with {}, you are Daisy:
"""

def appendBotMsg(botMsg):
    global conversation_history
    conversation_history = conversation_history + botMsg.strip() + "\n"

def appendUserMsg(userMsg):
    global conversation_history, user_details
    conversation_history = conversation_history + "> " + ("User" if user_details["name"] == "" else user_details["name"]) + ": " + userMsg.strip() + "\n> Daisy: "

def sendTxtMsg(msg):
    global user_details, conversation_history
    payload = json.dumps({
        "to": user_details["num"],
        "type": "text",
        "text": {
            "body": msg
        }
    })
    print(" > sendTxtMsg: ", msg)
    appendBotMsg(msg)
    print(" > DEBUG : CONVERSATION HISTORY", conversation_history)
    response = requests.request("POST", url, headers=headers, data=payload)

def sendImgMsg(img, caption):
    global user_details, conversation_history
    payload = json.dumps({
        "to": user_details["num"],
        "type": "image",
        "image": {
            "link": img,
            "caption": caption
        }
    })
    print(" > sendImgMsg: ", img, caption)
    appendBotMsg(caption)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def sendCatalogMsg(title, subtitle="", footer=""):
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
        # print(" > Generated Payload: ", payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        appendBotMsg(title + " [**INSERT_CATALOG_HERE**]")
        print(" > sendCatalogMsg: ", response.text)

def getOrderDetails(num):
    global headers, url, target_number, user_details, flag, conversation_history
    sendTxtMsg(order_details[num])
    
def initConversation():
    global headers, url, target_number, user_details, flag
    payload = json.dumps({
        "to": user_details["num"],
        "type": "image",
        "recipient_type": "individual",
        "image": {
            "link": "https://storiesflistgv2.blob.core.windows.net/stories/2019/03/article_banner_press_release_26_03_19_v1-01.jpg",
            "caption": "Welcome to Flipkart, I am Daisy, How may I help you today?"
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    appendBotMsg("Welcome to Flipkart, I am Daisy, How may I help you today?")
    flag = 1
    print(" > startConversation: Sent Greeting")

def setName(name):
    global user_details, conversation_history, flag
    try:
        stmt = name.strip().split(" ")
        if len(stmt) == 1:
            user_details["name"] = stmt[0]
            conversation_history.format(stmt[0])
            flag = 9
            return True
    except Exception as e:
        print(" > ERROR - setName: ", e)
        
    
    thisPrompt = """
    Marv is an AI assistant that is made to extract the User's name from a statement It returns "-1 **" if the user did not provide their name.
     > User: Hi, I am Jaynam
     > Marv: Jaynam **

     > User: My name is Aditi Kumar
     > Marv: Aditi Kumar **

     > User: who is elon musk
     > Marv: -1 **

     > User: My name
     > Marv: -1 **

     > User: {}
     > Marv:""".format(name)
    
    response = openai.Completion.create(
        model="text-davinci-003",
        max_tokens=5,
        prompt=thisPrompt,
        temperature=0.1,
        stop=["**"]
    )

    uName = response["choices"][0]["text"].strip()

    print(" > setName: ", uName)

    if uName == "-1":
        sendTxtMsg("Sorry, I did not get your name. Please try again.")
        return False
    else:
        user_details["name"] = uName
        conversation_history.format(uName)
        # usrMsg(name)
        flag = 9

def parseMsg(json_data):
        pprint("!!!!!!!!!!!!!")
        pprint(json_data)
        global user_details, conversation_history, flag      
        if "contacts" in json_data:
            try:
                data_type = json_data["messages"][0]["interactive"]["type"]
            except KeyError:
                data_type = "text"
            try:
                msg = json_data["messages"][0]["text"]["body"].lower()
            except KeyError:
                msg = json_data["messages"][0]["interactive"][data_type]["id"].lower()

            msg_to = json_data["contacts"][0]["wa_id"]

            user_details["num"] = msg_to

            print(" > Message received from: ", msg_to, " | Message: ", msg)
            appendUserMsg(msg)

            return msg
        if "statuses" in json_data:
            pprint(" > Last Message to: " + json_data["statuses"][0]["recipient_id"] + " | Status: " + json_data["statuses"][0]["status"])
            return "[**status**]"
        
def generatePrompt(userInput):
    global conversation_history
    # appendUserMsg(userInput)
    # conversation_history = conversation_history + userInput.strip() + "\nDaisy: "
    return conversation_history

def generateResponse(userInput):
    global conversation_history
    thisPrompt = generatePrompt(userInput)
    response = openai.Completion.create(
        model="text-davinci-002",
        max_tokens=50,
        prompt=thisPrompt,
        temperature=0.1,
        stop=["> User:"]
    )
    reply = response["choices"][0]["text"].strip()
    print(" > generateResponse: \n", conversation_history.split("\n")[-3:])
    # print(" !> debug:  ", )
    return reply

@csrf_exempt
def webhook(request):
    global flag, form_data, headers, url, target_number, user_details
    
    if request.method == 'POST':
        post_data = json.loads(request.body)

        user_msg = parseMsg(post_data)
        user_num = user_details["num"]

        if user_msg == "[**status**]":
            return HttpResponse("OK")

        if user_num not in target_numbers and target_numbers != []:
            print(" > Message not for me")
            return HttpResponse("Message not for me")
        
        if flag == 0:
            initConversation()
            sleep(2)
            sendCatalogMsg("Shopping Menu - Flipkart", "Hi there, welcome to our store, please choose a product you want to know more about:", "Click on view products to see!")
            return HttpResponse("Conversation Started")
        # elif flag == 1:
            # if setName(user_msg):
            # return HttpResponse("Name Set")
        elif flag != 0:
            raw_text = generateResponse(user_msg)
            prod_matches = re.findall(r"\[\*\*INSERT_PRODUCT=(\w+)\*\*\]", raw_text)
            if prod_matches != []:
                productId = prod_matches[0]
                raw_msg = raw_text.replace(f"[**INSERT_PRODUCT={productId}**]", "")
                sendImgMsg(images[productId], raw_msg + urls[productId])
            elif "[**INSERT_TRACKING_LINK_HERE**]" in raw_text:
                getOrderDetails(user_details["num"])
            elif "**INSERT_CATALOG_HERE**" in raw_text:
                sendCatalogMsg("Here are some products that you might like")
            else:
                sendTxtMsg(raw_text)
            return HttpResponse("Message Sent")
        else:
            return HttpResponse("Error: GET request")
         