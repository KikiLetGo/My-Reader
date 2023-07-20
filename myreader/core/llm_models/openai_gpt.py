import json
import http.client
from myreader.config.config import Config
class GPTModel:
	def __init__(self):
		pass
	def chat(self, messages):
		payload = {
			"model":"gpt-3.5-turbo",
			"messages":messages
		}
		payload = json.dumps(payload)


		conn = http.client.HTTPSConnection("api.openai.com")

		config = Config()
		auth = 'Bearer '+config.openai_api_key

		headers = {
			'Content-Type': 'application/json',
			'Authorization': auth
		}
		conn.request("POST", "/v1/chat/completions", payload.encode('utf-8'), headers)
		res = conn.getresponse()
		data = res.read().decode("utf-8")
		try:
			reply = json.loads(data)['choices'][0]['message']['content']
			return reply
		except KeyError:
			print("Key Error")
			print(data)
			return None

