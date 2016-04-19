# -*- coding: utf-8 -*-
import bot_config
import telebot
import time
import api
from datetime import datetime

def log(m, log):
	try:
		log.write('\t'.join([
			datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			str(m.chat.id),
			str(m.from_user.id),
			str(m.from_user.first_name) + ' ' + str(m.from_user.last_name),
			str(m.from_user.username),
			m.text]) + '\n')
	except:
		log.write('error\n')

def listener(messages):
	for m in messages:
		if m.content_type == 'text':
			log(m, log_file)
			bot.send_message(m.chat.id, api.main(m.text), parse_mode='HTML')

if __name__ == '__main__':
	with open('log.txt', 'a') as log_file:
		bot = telebot.TeleBot(bot_config.token)
		bot.set_update_listener(listener)
		bot.polling(none_stop=True)
		while True:
			time.sleep(200)