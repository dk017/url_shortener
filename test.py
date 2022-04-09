import os
import telebot
import urllib
import requests
import redis
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

my_secret = os.environ['API_KEY']
cutty_api_key = os.environ['CUTTY_API_KEY']
bot = telebot.TeleBot(my_secret)

re = redis.Redis(
    host=os.environ['HOST'],
    port=os.environ['PORT'],
    password=os.environ['PASSWORD'],
)


@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "hey! how's it going?")


@bot.message_handler(commands=['hello'])
def hello(message):
    chat_id = message.chat.id
    print('hey dhinesh')
    bot.send_message(chat_id, "hey! how's it going?")


@bot.message_handler(commands=['wsb'])
def get_stocks(message):
    response = ""
    stocks = ['gme', 'amc', 'nok']
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='2d', interval='1d')
        data = data.reset_index()
        response += f"-----{stock}-----\n"
        stock_data.append([stock])
        columns = ['stock']
        for index, row in data.iterrows():
            stock_position = len(stock_data) - 1
            price = round(row['Close'], 2)
            format_date = row['Date'].strftime('%m/%d')
            response += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)
        print()

    response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
    for row in stock_data:
        response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
    response += "\nStock Data"
    print(response)
    bot.send_message(message.chat.id, response)


def url_short_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "url":
        return False
    else:
        return True


# @bot.message_handler(func=url_short_request)
# def send_price(message):
#   request = message.text.split()[1]
#   data = yf.download(tickers=request, period='5m', interval='1m')
#   if data.size > 0:
#     data = data.reset_index()
#     data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
#     data.set_index('format_date', inplace=True)
#     print(data.to_string())
#     bot.send_message(message.chat.id, data['Close'].to_string(header=False))
#   else:
#     bot.send_message(message.chat.id, "No data!?")

@bot.message_handler(func=url_short_request)
def shorten_url(message):
    print("shorten url called")
    request_url = message.text.split()[1]
    print(request_url)
    chat_id = message.chat_id
    r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(cutty_api_key, request_url))
    if r.json()['url']['status'] != 7:
        update.message.reply_text("Please enter a valid URL")
    else:
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

        update.message.reply_text(shortened_link)
        if send_suggestion:
            update.message.reply_text(
                'Hope you are enjoying the tool!!!\n Consider buying me a coffee if you wish!!!',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text='BuyMeACoffee', url='https://www.buymeacoffee.com/dk17')],
                ])
            )


bot.polling()