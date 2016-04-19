# -*- encoding: utf-8 -*-
import requests
import json
import pickle
from datetime import datetime


# read saved license from a file
with open('session.pickle', 'rb') as f:
	session = pickle.load(f)

apiurls = {
	'status': 'https://api.glvrd.ru/v2/status/',
	'session': 'https://api.glvrd.ru/v2/session/',
	'proofread': 'https://api.glvrd.ru/v2/proofread/',
	'hints': 'https://api.glvrd.ru/v2/hints/'
}

params = {
	'app': 'glavredbot/alpha',
	'session': session
}

data = {}

def getSessionId():
	new_session_id = json.loads(requests.post(apiurls['session'], params=params).text)['session']
	params['session'] = new_session_id
	with open('session.pickle', 'wb') as f:
		pickle.dump(new_session_id, f)
	with open('sessions_log.txt') as log_f:
		log_f.write('\t'.join([
			str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
			new_session_id
		]) + '\n')

def prepareOutcome(answer):
	if len(answer['fragments']) == 0:
		outcome = 'Ок'

	else:
		# collect ids of hints
		data['ids'] = ','.join([f['hint_id'] for f in answer['fragments']])
		# get hints
		hints = json.loads(requests.post(apiurls['hints'], params=params, data=data).text)['hints']
		# get text and print mistakes along with hints
		for h in hints:
			for f in answer['fragments']:
				if f['hint_id'] == h:
					hints[h]['word'] = answer['text'][f['start']:f['end']]
		hints_formatted = [' — '.join([hints[h]['word'], '<b>'+hints[h]['name']+'</b>', hints[h]['description']]) for h in hints]
		outcome = '\n\n'.join(hints_formatted).replace('&nbsp;', ' ')

	return outcome

def main(text):
	if text == '':
		result = 'Пустой запрос'

	else:
		data['text'] = text

		# send request to Glavred
		answer = json.loads(requests.post(apiurls['proofread'], params=params, data=data).text)
		
		if answer['status'] == 'ok' and 'fragments' in answer:
			answer['text'] = text
			result = prepareOutcome(answer)


		# if session id is old
		elif answer['status'] != 'ok' and answer['code'] == 'missing_param' and answer['name'] == 'session':
			print('old session id %s! asking for new...' % (params['session']))
			del params['session']

			new_session_id = json.loads(requests.post(apiurls['session'], params=params).text)['session']
			params['session'] = new_session_id

			getSessionId()
			
			result = main(text)

		# if unexpected problem
		else:
			print(answer)
			result = 'unexpected outcome — printed above'

	return result

if __name__ == '__main__':
	# print(checkText('качественный текст для проверки. наверное, будет качественный результат'))
	print(main('Сделал альфа-версию бота. Пока умеет только отправлять текст в Главред и тупо копировать ошибки из ответа. Надо много работать над структурой ответа, тестировать и вообще.'))