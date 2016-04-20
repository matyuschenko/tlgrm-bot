# -*- coding: utf-8 -*-
import bot_config
import telebot
import api
from datetime import datetime
import botan


# function to log requests
def log(m):
	with open('log.txt', 'a') as log_file:
		try:
			msg = '\t'.join([
				datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				str(m.chat.id),
				str(m.from_user.id),
				str(m.from_user.first_name) + ' ' + str(m.from_user.last_name),
				str(m.from_user.username),
				m.text.replace('\n', '\\n')])
			print(msg)
			log_file.write(msg + '\n')
		except:
			log_file.write('error\n')


#set my bot
bot = telebot.TeleBot(bot_config.token)


#message handlers - descriptors to process certain scenarios
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	log(message)
	bot.reply_to(message, bot_config.help_message)

@bot.message_handler(commands=['settings'])
def handle_start_help(message):
	log(message)
	bot.reply_to(message, bot_config.settings_message)

@bot.message_handler(func=lambda m: True, content_types=['text'])
def process_msg (message):
	log(message)
	botan.track(bot_config.botan_token, message.chat.id, message)
	bot.reply_to(message, api.main(message.text), parse_mode='HTML')


#start bot
if __name__ == '__main__':
	bot.polling(none_stop=True)