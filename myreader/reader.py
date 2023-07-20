from myreader.core.embbedings import Embbeding
from myreader.core.vec_searcher import VecSearcher
from myreader.core.prompts.prompt import Prompt
from myreader.core.llm_models.openai_gpt import GPTModel
from myreader.utils import hash_utils
from myreader.core.token_counter import count_string_tokens

import numpy as np

class Reader:
	def __init__(self):
		self.vec_searcher = VecSearcher()
		self.maps = {}
		self.llm_model = GPTModel()
		self.chunk_min_size = 500
		self.max_token = 3800#TODO：研究下open ai中文的token计算规则，做的精确些


	def split_into_segments(self, novel, target_length):
		segments = []
		start = 0
		end = start + target_length
		length = len(novel)
		while start < length:
			# 向前搜索，找到一个完整的句子或段落作为片段
			while end < length and novel[end-1] not in ['。', '！', '？']:
				end += 1

			if novel[start:end].count('“') > novel[start:end].count('”'):
				# 向前搜索，找到对话结束的引号
				while end < length and novel[end-1] not in ['”']:
					end += 1

			# 添加当前片段到列表中
			segment = ''.join(novel[start:end])
			segments.append(segment)

			# 移动窗口到下一个位置
			start = end
			end = start + target_length
			if end >= length:
				end = length


		return segments

	def read(self, path):
		with open(path, 'r', encoding='utf-8') as file:
			contents = file.read()
			chunks = self.split_into_segments(contents, self.chunk_min_size)
			print("chunks length:%d"%len(chunks))

			"""
			Embedding all segments into vector data
			
			Use the md5 hash as the cache name,so ever change of book and the way of chunks spliting
			will regenerate vecs and update caches
			"""
			cache_file = hash_utils.md5(str(chunks)) + ".json"
			embedding = Embbeding(cache_file=cache_file)
			vec_data = embedding.texts2vecs(chunks)

			vectors=[]
			for data in vec_data:
				vectors.append(data['embedding'])
				self.maps[str(data['index'])]=chunks[data['index']]

			self.vec_searcher.add(np.array(vectors))


	def ask(self):
		embedding = Embbeding()
		while True:
			ask = input("ask:")
			if "quit" == ask:
				exit()
			vector = embedding.text2vec(ask)
			if vector is None:
				continue

			k = int(self.max_token/self.chunk_min_size)
			print('search topK:%d' % k)

			D, I = self.vec_searcher.search(np.array([vector]),k)

			relate_segs = []
			for i in I[0]:
				
				#print('=========================')
				seg = self.maps[str(i)]
				relate_segs.append(seg)
				#print(seg)
				#print('=========================')

			prompt = Prompt()
			messages = prompt.build()
			segs_msg={
				"role":"user",
				"content":"相关内容片段有这些：" + str(relate_segs)
			}
			messages.append(segs_msg)

			question_msg = {
				"role":"user",
				"content":"问题是："+ask
			}
			messages.append(question_msg)


			# delete char util match token limit
			token_counts = count_string_tokens(str(messages))
			print('[before]message char counts:%d' % len(str(messages)))

			print("token_counts:%d" % token_counts)
			while token_counts > self.max_token:
				relate_segs = messages[len(messages)-2]['content']
				messages[len(messages)-2]['content'] = relate_segs[0:(len(relate_segs)-5)]
				token_counts = count_string_tokens(str(messages))
				#print("token_counts:%d" % token_counts)


			print('[after]message char counts:%d' % len(str(messages)))

			reply = self.llm_model.chat(messages)
			print(reply)

				
