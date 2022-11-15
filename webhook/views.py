from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
# from gtts import gTTS
import json
from pprint import pprint
import requests
import openai

openai.api_key = "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"
#os.getenv("OPENAI_API_KEY")

# conversation_history = """
# Marv is a friendly chatbot that answers questions with cheerful responses:

# You: How many pounds are in a kilogram?
# Marv: There are 2.2 pounds in a kilogram, let me know if you need more help.
# You: What does HTML stand for?
# Marv: A search from google says it stands for hypertext markup language, hope this solves your query.
# You: When did the first airplane fly?
# Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights.
# You: What is the meaning of life?
# Marv: I’m not sure. I’ll ask my friend Google.
# You: 
# """

summarization_api_key = "6562713e-5f93-41cd-870c-c0c9144a511b"

conversation_history = """
Marv is a friendly chatbot that answers questions with cheerful responses based on given input, read the following article and continue the conversation that follows:
Article:
Consumer inflation eased in October. The year-over-year was the smallest since the start of the year. The inflation numbers were lower than what most economists had expected. Let us look at the details and what it means for investors. The Bureau of Labor Statistics released the CPI data for October - the US inflation has come to 7.7%. In September, inflation was 8.2%, while in August, the annual increase was 8.3%. The CPI for all Urban Consumers (CPI-U) increased by 0.4% in October on a seasonally adjusted basis (same increase as September). The all-items index increased by 7.7% before the seasonal adjustment. The increase in October is the smallest 12-month increase since the start of 2022. All items, excluding the food and energy index (called core inflation), increased by 6.3%. The expectation was the core inflation would increase by 6.5%, while the headline inflation would increase by 7.9%. Federal Reserve may slow rate hikes: The Federal Reserve said in the last meeting that it plans to bring inflation under control, and for that, it will continue to increase rates. However, now that inflation has lowered, even though, marginally, it opens the way for the Fed to slow its aggressive interest rate hikes. If that happens, the equity market will benefit.

Stocks and crypto surge: Post the inflation numbers and expectation that Fed will now try to avoid a hard landing on the economy, the US equity market surged. The major indices reported their best daily gains since 2020. The NASDAQ rallied over 7%. Even the largest cryptocurrency recovered some of its losses and was up 3%, nearing the $18000-mark.

Dollar index fall: The US dollar index dipped by 1.96%, with the euro climbing by 1.55%. Notably, the dollar also tumbled against the Japanese yen, making a move toward its biggest one-day dive since 2016. 

Crude oil price increase: Crude oil prices nudged upward due to the better-than-expected US inflation numbers. Hopes for steady demand take rounds, which is expected to offset the impact of Covid restrictions in China. US crude rose by over 1% and traded around $86.8 per barrel late Thursday.

What should investors do?
Post the October inflation numbers, the US market rallied, and the Indian market did the same on Friday. However, investors should not try to time the market, assuming the rally will continue. Experts suggest, amid high interest rate environment, growth stocks in cloud, e-tailers and software sectors may continue to remain under pressure due to concerns over their valuation. Companies which can maintain healthy margins due to their pricing power will be relative outperformers. 

Avoid lump sum allocation and adopt a more staggered approach while investing in equities over the next few months. US stocks SIP’s are the best way to take advantage of volatility. Invest through INDmoney at zero additional cost.

This is not an investment advisory. The blog is for information purposes only. Investments in the securities market are subject to market risks, read all the related documents carefully before investing. Past performance is not indicative of future returns. Please consider your specific investment requirements, risk tolerance, goal, time frame, risk and reward balance, and the cost associated with the investment before choosing a fund, or designing a portfolio that suits your needs. The performance and returns of any investment portfolio can neither be predicted nor guaranteed. 

Human: Hi marv, how are you?
Marv: Hello there, how may I help you?
Human: """
def generatePrompt(userInput):
    global conversation_history
    conversation_history = conversation_history + userInput.strip() + "\nMarv: "
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
    conversation_history = conversation_history + reply + "\nYou: "
    # print(" !> debug:  ", )
    return reply


@csrf_exempt
def webhook(request):
    global flag, form_data
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
                msg = data_sent["messages"][0]["interactive"]["button_reply"]['title'].lower()
            msg_to = data_sent["contacts"][0]["wa_id"]
            if msg_to != "917990326788":
                return HttpResponse(" > Not your number")
            print(data_sent)
            if msg != "":
                payload = json.dumps({
                    "to": msg_to,
                    "type": "text",
                    "text": {
                        "body": generateResponse(msg)
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)
        return HttpResponse("Webhook received!")
    elif request.method == 'GET':
        print(" > Get request received")
        return HttpResponse("Webhook received!")