import os
import telebot

my_secret = "5194362531:AAErLinj_fm6qjqlvox1w9v6xEky8dgpus4"
bot = telebot.TeleBot(my_secret)
@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "hey! how's it going?")

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.reply_to(message.chat.id, "hey! how's it going?")

bot.polling()