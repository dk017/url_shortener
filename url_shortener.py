import telebot
import requests
import redis
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import os


# my_secret = os.environ['API_KEY']
# cutty_api_key = os.environ['CUTTY_API_KEY']

PORT = int(os.environ.get('PORT', 5000))
bot = telebot.TeleBot("5194362531:AAErLinj_fm6qjqlvox1w9v6xEky8dgpus4")
cutty_api_key = "3e8274e7feaf9eaaf909be641a1ca15691b7b"
re = redis.Redis(
    host="redis-11024.c8.us-east-1-3.ec2.cloud.redislabs.com",
    port="11024",
    password="6GxkgPwOWUUlm1cSINg8XnWGgPBfS4te"
)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(text='BuyMeACoffee', url='https://www.buymeacoffee.com/dk17'))
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hey ' + message.from_user.first_name + '!!!!')


@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "url ")


def url_short_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "url":
        return False
    else:
        return True


@bot.message_handler(func=lambda m: True)
def shorten_url(message):
    request_url = message.text

    if not request_url.startswith("http"):
        request_url = 'https://' + message.text
    shorten_url_util(request_url, message)


def shorten_url_util(url, message):
    chat_id = message.chat.id
    send_suggestion = False
    r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(cutty_api_key, url))
    if r.json()['url']['status'] == 7:
        shortened_link = r.json()['url']['shortLink']
        count = int(re.get(chat_id))
        if count is not None:
            count = count + 1
            if count % 10 == 0:
                send_suggestion = True
            re.set(chat_id, count)
            print(count)
        else:
            re.set(chat_id, 1)

        bot.send_message(chat_id, text=shortened_link)
        if send_suggestion:
            bot.send_message(
                chat_id,
                text='Hope you are enjoying the tool!!!\nConsider buying me a coffee if you wish!!!',
                reply_markup=gen_markup()
            )
    elif r.json()['url']['status'] == 2:
        bot.send_message(chat_id, 'Please mention a valid url')

    elif r.json()['url']['status'] == 5:
        bot.send_message(chat_id, 'Provided link contains invalid characters')
    else:
        bot.send_message(chat_id, 'Hey ' + message.from_user.first_name + ' Not able to shorten this link.')
        bot.send_message(chat_id, 'Please retry or try with a different URL.')


bot.set_webhook(url="https://dk-url-shorted.herokuapp.com/"+"5194362531:AAErLinj_fm6qjqlvox1w9v6xEky8dgpus4")
bot.polling()
