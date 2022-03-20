import requests
import time
import json

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update

# list of quotes
# quotes = [
#     'First, solve the problem. Then, write the code. – John Johnson',
#     'Experience is the name everyone gives to their mistakes. – Oscar Wilde',
#     'Code is like humor. When you have to explain it, it’s bad. – Cory House',
#     'Before software can be reusable it first has to be usable. – Ralph Johnson',
#     'Optimism is an occupational hazard of programming: feedback is the treatment. - Kent Beck'
# ]
quotes = [
    'hey dhinesh',
    'hello preetha'
]

telegram_bot_token = "5173482597:AAGq28BsTbHO6XG-iuJjCkDk9l7Dqv_sC9I"
#
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

bot = telegram.Bot(token=telegram_bot_token)

bot.send_message(text='Hey Dhinesh', chat_id=553624378)


# loop through the quotes
# for quote in quotes:
#     url = 'https://api.telegram.org/bot5173482597:AAGq28BsTbHO6XG-iuJjCkDk9l7Dqv_sC9I/sendMessage?chat_id=553624378' \
#           '&text="{}"'.format(quote)
#     requests.get(url)
#     # sends new quotes every 20seconds
#     time.sleep(2)
#

#
# def random():
#     # fetch data from the api
#     response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
#     data = response.json()
#     # send message
#     bot.send_message(chat_id=553624378, text=data['quote'])
#
#
# random()

def start(update: Update, context: CallbackContext):
    print("called")
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


