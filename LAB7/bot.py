import telebot
from telebot import types
from cls import *

bot = telebot.TeleBot('your token')

@bot.message_handler(commands=['start'])
def start(message):
	# Первое сообщение бота
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('/help')
	bot.send_message(message.chat.id,information.start, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('/abitur','/contacts','/mtuci')
	bot.send_message(message.chat.id,information.help, reply_markup=keyboard)

@bot.message_handler(commands=['abitur'])
def abitur(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('/help')
	bot.send_message(message.chat.id,information.abitur, reply_markup=keyboard)

@bot.message_handler(commands=['contacts'])
def contacts(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('/help')
	bot.send_message(message.chat.id,information.contacts, reply_markup=keyboard)

@bot.message_handler(commands=['mtuci'])
def mtuci(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add('/help')
	bot.send_message(message.chat.id,information.mtuci, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def answer(message):
	if message.text.lower() == 'привет':
		start(message)
	if message.text.lower() == 'как дела?':
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add('/help')
		bot.send_message(message.chat.id,information.answer1,reply_markup=keyboard)
	if message.text.lower() == 'спишь?':
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add('/help')
		bot.send_message(message.chat.id,information.answer2,reply_markup=keyboard)

if __name__ == '__main__':
    bot.polling(none_stop=True)