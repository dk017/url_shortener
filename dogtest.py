from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re


def get_url():
    print("get called")
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    print(url)
    return url


def bop(update, context):
    url = get_url()
    chat_id = update.message.chat_id
    print(chat_id)
    context.bot.sendPhoto(chat_id, url)
    context.bot.sendMessage(text="preetha oru loosu", chat_id=chat_id)
    print(type(context.bot))



def main():
    updater = Updater('5173482597:AAGq28BsTbHO6XG-iuJjCkDk9l7Dqv_sC9I')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()