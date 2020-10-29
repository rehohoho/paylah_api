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

from config import TELEBOT_TOKEN, HEROKU_URL, \
    DBS_CLIENT_ID, AUTH_CODE_B64, DBS_REDIRECT_URL, \
    DBS_AUTH_URL

AUTH_TOKEN = ""

global bot
bot = telegram.Bot(token=TELEBOT_TOKEN)
app = Flask(__name__)


def start(chat_id):
    text = ("You need to authenticate with DBS.")
    
    url = "%s?client_id=%s&redirect_uri=%s&scope=Read&response_type=code&state=0399" %(
        DBS_AUTH_URL, DBS_CLIENT_ID, DBS_REDIRECT_URL)
    
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

    return 'ok'


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