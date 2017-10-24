import os, sys
from flask import Flask, request
from pymessenger import Bot


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAEDZCznWAZAIBADLUhw1yOmt8O3Qo7zZA2DGGYVFZBpR4SnyHkrDS2U3HTGZAkzLLE73StIFAQHHJ1pOynRdHyYHIK7fhWQP2oZBAwP5eBs3ldZBOaUzD2sMzIEqvm98YlqFXucHZAdRRfhPtVPKQkE15MDMwaoycJrWCvdRnjqCgZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook,  it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'hello':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/', methods=['POST'])
def weebhook():
    data=request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # ID
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                        if messaging_text.lower() in ['hi', 'hello', 'hey']:
                            response = "Hello User !! How are You ? "
                        else:
                            response = messaging_text

                else:
                    messaging_text = ''
                bot.send_text_message(sender_id, response)
    return "ok", 200

def log(msg):
    print(msg)
    sys.stdout.flush()


if (__name__ == "__main__"):
    app.run(debug = True, port = 8000)
