import os
from myreader.reader import Reader

def main():
	reader = Reader()
	book_path  = input("(Only txt file support now)Input the path of book:")
	while not os.path.exists(book_path):
		book_path  = input("File not exists,please input correct path:")

	reader.read(book_path)
	reader.ask()
	
