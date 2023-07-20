import os
from dotenv import load_dotenv

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class Config:
	def __init__(self):
		load_dotenv()
		self.openai_api_key = os.getenv("OPENAI_API_KEY")
