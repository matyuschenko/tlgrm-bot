# -*- coding: utf-8 -*-
import bot_config
import telebot
import time

def listener(messages):
	for m in messages:
		if m.content_type == 'text':
			bot.send_message(m.chat.id, m.text)

if __name__ == '__main__':
	bot = telebot.TeleBot(bot_config.token)
	bot.set_update_listener(listener)
	bot.polling(none_stop=True)
	while True:
		time.sleep(30)