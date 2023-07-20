import faiss
class VecSearcher:
	def __init__(self):
		self.d = 1536 # vector size
		self.M = 32 # the number of neighbors we add to each vertex on insertion
		self.index = faiss.IndexHNSWFlat(self.d, self.M)
		print(self.index.hnsw)
	def add(self, xb):
		self.index.add(xb)
	def search(self, xq, k):
		D, I = self.index.search(xq, k)
		print("======D=====")
		print(D)
		print("======I=====")
		print(I)
		return D, I