"""
Hm
"""

import urllib.parse
import logging

from flask import Flask, request

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, Filters
from telegram.utils import helpers

DBS_CLIENT_ID = "b2c8c8c5-2291-4cda-a936-ee273e812c48"
DBS_CLIENT_SECRET = "60838a10-e083-4dd7-bd01-9dd951f25ae6"
DBS_AUTH_URL = "https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize"
DBS_REDIRECT_URL = "https://www.dbs.com/developer/#/all-products/play-ground"

TELEBOT_TOKEN = "1395910915:AAG8iA2bYXrsQvcVPDOdIv-_Avht875vPEc"

AUTH_REPLY_DEEPLINK = "AUTH_REPLY"

HEROKU_URL = "https://please-let-me-test-bot.herokuapp.com/"


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# cannot be used since chat id can differ
# https://api.telegram.org/bot1395910915:AAG8iA2bYXrsQvcVPDOdIv-_Avht875vPEc/sendMessage?chat_id=1066547412&text=?123./124`

app = Flask(__name__)

@app.route('/{}'.format(TELEBOT_TOKEN), methods=['POST'])
def respond():
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
       # print the welcoming message
       bot_welcome = """
       Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


   else:
       try:
           # clear the message we got from any non alphabets
           text = re.sub(r"W", "_", text)
           # create the api link for the avatar based on http://avatars.adorable.io/
           url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

   return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=HEROKU_URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)

# def start(update, context):
    
#     print(context.args)
#     print(update.effective_chat.id)
    
#     bot = context.bot
#     text = ("You need to authenticate with DBS.")
#     # orig_url = helpers.create_deep_linked_url(bot.get_me().username, AUTH_REPLY_DEEPLINK)
#     orig_url = helpers.create_deep_linked_url(bot.get_me().username)
#     # orig_url = DBS_REDIRECT_URL
#     redirect_url = urllib.parse.quote(orig_url, safe="")
    
#     print(orig_url)
#     print(redirect_url)

#     url = "%s?client_id=%s&redirect_uri=%s&scope=Read&response_type=code&state=0399" %(
#         DBS_AUTH_URL, DBS_CLIENT_ID, redirect_url)
    
#     keyboard = InlineKeyboardMarkup.from_button(
#         InlineKeyboardButton(text="Authenticate", url=url)
#     )
#     update.message.reply_text(text, reply_markup=keyboard)


# def receive_auth_key(update, context):
#     print("receive auth key was called")
#     print(context.args)


# def auth_reply_deep_link(update, context):
#     payload = context.args
#     update.message.reply_text(
#         "The payload was: {}".format(payload)
#     )


# def main():

#     # Create the Updater and pass it your bot's token.
#     updater = Updater(TELEBOT_TOKEN, use_context=True)
#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher

#     dp.add_handler(CommandHandler("start", auth_reply_deep_link, Filters.regex(AUTH_REPLY_DEEPLINK)))
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("code", receive_auth_key, pass_args=True))
    
#     updater.start_polling()
#     updater.idle()


# if __name__ == "__main__":
#     main()