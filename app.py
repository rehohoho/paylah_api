"""
Main app to be run by Heroku

DBS_REDIRECT_URL has to correspond to app configuration in DBS developer's portal
"""

import urllib.parse
import logging
import re

from flask import Flask, request
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

TELEBOT_TOKEN = "1395910915:AAG8iA2bYXrsQvcVPDOdIv-_Avht875vPEc"
HEROKU_URL = "https://please-let-me-test-bot.herokuapp.com/"

DBS_CLIENT_ID = "b2c8c8c5-2291-4cda-a936-ee273e812c48"
DBS_CLIENT_SECRET = "60838a10-e083-4dd7-bd01-9dd951f25ae6"
DBS_AUTH_URL = "https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize"
DBS_REDIRECT_URL = "{heroku_url}{telebot_token}/receive_access_token/".format(
    heroku_url=HEROKU_URL, telebot_token=TELEBOT_TOKEN)

AUTH_TOKEN = ""

global bot
bot = telegram.Bot(token=TELEBOT_TOKEN)
app = Flask(__name__)


def start(chat_id):
    text = ("You need to authenticate with DBS.")
    redirect_url = urllib.parse.quote(DBS_REDIRECT_URL, safe="")
    
    print(DBS_REDIRECT_URL)
    print(redirect_url)
    
    url = "%s?client_id=%s&redirect_uri=%s&scope=Read&response_type=code&state=0399" %(
        DBS_AUTH_URL, DBS_CLIENT_ID, redirect_url)
    
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="Authenticate", url=url)
    )
    bot.sendMessage(chat_id=chat_id, text=text, reply_markup=keyboard)


@app.route('/{}'.format(TELEBOT_TOKEN), methods=['POST'])
def respond():
    print("respond")
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()

    # for debugging purposes only
    print("got text message :", text)

    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        start(chat_id)

#    else:
#        try:
#            # clear the message we got from any non alphabets
#            text = re.sub(r"W", "_", text)
#            # create the api link for the avatar based on http://avatars.adorable.io/
#            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
#            # reply with a photo to the name the user sent,
#            # note that you can send photos by url and telegram will fetch it for you
#            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
#        except Exception:
#            # if things went wrong
#            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

    return 'ok'


# https://please-let-me-test-bot.herokuapp.com/1395910915:AAG8iA2bYXrsQvcVPDOdIv-_Avht875vPEc/?code=Eiivy%2Bui2oY4fnxXeO3csdwHtGw%3D&state=0399
@app.route('/{}/receive_access_token/'.format(TELEBOT_TOKEN))
def receive_access_token():
    if "code" in request.args:
        code = request.args["code"]

    AUTH_TOKEN = code

    return "Authentication token is {code}".format(code=code)


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    print("set_webhook")
    s = bot.setWebhook('{url}{hook}'.format(url=HEROKU_URL, hook=TELEBOT_TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)