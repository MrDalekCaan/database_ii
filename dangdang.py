import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading
from time import sleep
# import chardet

url = "http://category.dangdang.com/cp01.77.01.00.00.00.html"
# book[id, bookname, imgurl, author, price]

def has_key(dict, key):
	return key in dict.keys()

def getbooks(url)->list:
	for _ in range(30):
		try:
			r = requests.get(url, timeout=10)
		except requests.exceptions.ConnectionError:
			sleep(10)
			continue

		if r.status_code == 200:
			break
	if r.status_code != 200:
		return []

	print(f'get from {url}')


	soup = BeautifulSoup(r.text, "html.parser")
	ul = soup.find_all("ul", class_="bigimg")
	if len(ul) != 1:
		raise Exception(f"length of ul is {len(ul)}")
	ul = ul[0]

	lis = ul.find_all("li")
	books = []
	i = 0
	for li in lis:
		# print(i)
		# i += 1
		book = []
		books.append(book)
		# id
		book.append(li.attrs["id"])
		lias = li.find_all("a")
		# book name
		book.append(lias[0].attrs['title'])
		# img url
		if has_key(lias[0].find("img").attrs, 'data-original'):
			book.append(lias[0].find("img").attrs['data-original'])
		else:
			book.append(lias[0].find("img").attrs['src'])
		# author
		search_book_author = li.find("p", class_="search_book_author")
		spans = search_book_author.find_all("span")
		result = spans[0].find('a')
		if result is not None:
			book.append(result['title'])
		else:
			book.append('')
		# price
		book.append(li.find('p', class_='price').find('span', class_='search_now_price').text)
	return books

def cats():
	url = 'http://category.dangdang.com/?ref=www-0-C'
	all_books_cats = {}

	r = requests.get(url, timeout=10)
	for _ in range(5):
		r = requests.get(url, timeout=10)
		if r.status_code == 200:
			break
	if r.status_code != 200:
		return []

	soup = BeautifulSoup(r.text, "html.parser")
	classify_kinds = soup.find('div', id='floor_1').find_all('div', class_='classify_kind')

	for classify_kind in classify_kinds:
		cats = classify_kind.select('ul>li')
		del cats[-1]
		for cat in cats:
			a = cat.find('a')
			all_books_cats[a.text] = a['href']

	return all_books_cats

def page(link, page):
	if page < 0 or page > 100:
		return None
	return link[:29] + f'pg{page}-' + link[29:]



def thread_func(url, cat):
	books = []
	cat = cat.replace('/', '-')
	for p in range(1, 10):
		link = page(url, p)
		if link is  None:
			continue
		books += getbooks(link)
	df = pd.DataFrame(books, columns=['id', 'bookname', 'imgurl', 'author', 'price'])
	df.to_csv(f'/Users/dalek/Documents/working space/shity things/database/ii/csv/{cat}.csv', header=True)

def just10page():
	all_books_cats = cats()
	# threads = []
	for key in all_books_cats:
		t = threading.Thread(target=thread_func, args=(all_books_cats[key], key))
		t.start()
		t.join()
		# threads.append(t)


	# for t in threads:
	# 	t.join()

if __name__ == '__main__':
	just10page()
	# df = pd.DataFrame(getbooks(url), columns=['id', 'bookname', 'imgurl', 'author', 'price'])
	# print(df['imgurl'])

	# all_books_cats = cats()
	# print(len(all_books_cats))
	# for key in all_books_cats:
	# 	print(key, all_books_cats[key])





