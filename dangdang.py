import requests
import codecs
import os
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import re
# import threading
from time import sleep
import json
import random
# import chardet
# HTTPConnectionPool(host='127.0.0.1', port=1081)

url = "http://category.dangdang.com/cp01.77.01.00.00.00.html"
# book[id, bookname, imgurl, author, price]

def has_key(dict, key):
	return key in dict.keys()

def re_strip(string, char="\s"):
    result = re.sub(f"^{char}+", "", string)
    result = re.sub(f"{char}+$", "", result)
    return result

def request_url(url):
	status = True
	try:
		r = requests.get(url, timeout=10)
	except:
		status = False
	if status and r.status_code == 200:
		return r.text
	try:
		r = urllib.request.urlopen(url, timeout=10)
	except:
		return None
	if r.getcode() == 200:
		charset = r.headers.get_content_charset()
		if charset == 'gb2312':
			charset = 'gbk'
		try:
			return r.read().decode(charset)
		except:
			return None
	return None

def get_shop_info(product_main):
	"""
	div.product_main
	return
	-------
		[shopId, shop_name] if success
		None if failed
	"""
	a_link = product_main.select('span.title_name>span>a')
	if len(a_link) == 1:
		a_link = a_link[0]
	else:
		contents = product_main.select('span.title_name>span')
		text = ''
		for content in contents:
			text = content.text
		if '当当自营' in text:
			return ['0', '当当自营']
		else:
			return None
	if not a_link.has_attr('dd_name'):
		return None
	shopinfo = None
	try:
		shopinfo = [a_link['href'].split('/')[-1], a_link['title']]
	except:
		return None
	return shopinfo

def get_img_url(product_main):
	"""
	div.product_main
	return
	-------
		an url for image if success
		None if failed
	"""
	try:
		img = product_main.select('#largePic')[0]
		img_url = img['src']
	except:
		return None
	return img_url

def get_messbox_info(product_main):
	"""
	sometimes product_main doesn't have div.messbox_info
	return value will be none for that
	return
	-------
	dict{'author':'', 'publisher':'', 'publish_time':''}
	None
	"""
	info = {}
	try:
		messbox_info = product_main.select('div.messbox_info')[0]
		spans = messbox_info.find_all('span')
		for span in spans:
			if span.has_attr('dd_name'):
				if span['dd_name'] == '作者':
					info['author'] = span.find('a').text
				elif span['dd_name'] == '出版社':
					info['publisher'] = span.find('a').text
			else:
				# this may be time or something else
				content = span.text
				if '出版时间:' in content:
					publish_time = content.split('出版时间:')[-1]
					publish_time = re.sub(r'[^年月日0-9]', '', publish_time)
					publish_time = re.sub(r'[年月日]', '-', publish_time).strip('-')
					info['publish_time'] = publish_time
		if len(info.keys()) == 0:
			return None
		else:
			return info
	except:
		return None

def get_price(product_main):
	"""
	return
	------
		price or None
	"""
	dd_price = product_main.select('p#dd-price')
	if len(dd_price) == 1:
		return dd_price[0].contents[-1].strip()
	else:
		return None

def get_clearfix(clearfix):
	"""
	return
	-------
	dict{'kaiben':'', 'paper_type':'', 'pack':'', 'ISBN':'', 'is_suit':''}
	Won't return None
	"""
	s = str(clearfix)
	base_info = {'kaiben':'', 'paper_type':'', 'pack':'', 'ISBN':'', 'is_suit':''}
	search_result = re.search(r'> *开 ?本[:：]([^<]*)', s)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['kaiben'] = search_result.group(1)
	search_result = re.search(r'> *纸 ?张[:：]([^<]*)', s)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['paper_type'] = search_result.group(1)
	search_result = re.search(r'> *包 ?装[:：]([^<]*)', s)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['pack'] = search_result.group(1)
	search_result = re.search(r'ISBN[:：]([^<]*)', s)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['ISBN'] = search_result.group(1)
	search_result = re.search(r'> *是否套装[:：]([^<]*)', s)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['is_suit'] = search_result.group(1)
	return base_info

def get_base_info(productId, shopId, categoryPath):
	"""
	return
	-------
		dict{'book_name':'', 'ISBN': '', 'publisher':'','publish_time':'','author':'','price':'',
		'zhuangzhen':'','kaiben':'','weight':'','paper_count':''}
		None if failed to get base_info
	"""
	base_url = f"http://product.dangdang.com/index.php?r=callback%2Fdetail&productId={productId}&templateType=publish&describeMap=&shopId={shopId}&categoryPath={categoryPath}"
	base_info = {'book_name':'', 
						'ISBN': '', 
						'publisher':'',
						'publish_time':'',
						'author':'',
						'price':'',
						'zhuangzhen':'',
						'kaiben':'',
						'weight':'',
						'paper_count':''}
	r = request_url(base_url)
	try:
		r = json.loads(r)['data']['html']
		# sleep(random.randint(4, 10))
	except:
		return base_info
		# r = codecs.decode(r, 'unicode_escape')
	# if html:
	soup = BeautifulSoup(r, "html.parser")
	r = soup.text.replace('\xa0', ' ')

	search_result = re.search(r'书\s*名\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['book_name'] = search_result.group(1)
	search_result = re.search(r'ISBN\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['ISBN'] = search_result.group(1)
	search_result = re.search(r'出版社\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['publisher'] = search_result.group(1)
	search_result = re.search(r'出版时间\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['publish_time'] = search_result.group(1)
	search_result = re.search(r'出版日期\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1 and base_info['publish_time'] == '':
		base_info['publish_time'] = search_result.group(1)
	search_result = re.search(r'作\s*者\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['author'] = search_result.group(1)
	search_result = re.search(r'定\s*价\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['price'] = search_result.group(1)
	search_result = re.search(r'装\s*帧\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['zhuangzhen'] = search_result.group(1)
	search_result = re.search(r'开\s*本\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['kaiben'] = search_result.group(1)
	search_result = re.search(r'商品重量\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['weight'] = search_result.group(1)
	search_result = re.search(r'页\s*数\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1:
		base_info['paper_count'] = search_result.group(1)
	search_result = re.search(r'页\s*码\s*[:：]([^\s]*)', r)
	if search_result is not None and len(search_result.groups()) == 1 and base_info['paper_count'] == '':
		base_info['paper_count'] = search_result.group(1)

	if base_info['publish_time'] != '':
		base_info['publish_time'] = re_strip(base_info['publish_time'], '[^0-9]')
		base_info['publish_time'] = re.sub(r'[^0-9]', '-', base_info['publish_time'])

	return base_info
'''
	search_result = re.search('> *书名[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['book_name'] = search_result.group(1)
	search_result = re.search('> *ISBN[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['ISBN'] = search_result.group(1)
	search_result = re.search('> *出版社[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['publisher'] = search_result.group(1)
	search_result = re.search('> *出版时间[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['publish_time'] = search_result.group(1)
	search_result = re.search('> *出版日期[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1 and base_info['publish_time'] is not '':
		base_info['publish_time'] = search_result.group(1)
	search_result = re.search('> *作者[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['author'] = search_result.group(1)
	search_result = re.search('> *定价[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['price'] = search_result.group(1)
	search_result = re.search('> *装帧[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['zhuangzhen'] = search_result.group(1)
	search_result = re.search('> *开本[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['kaiben'] = search_result.group(1)
	search_result = re.search('> *商品重量[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['weight'] = search_result.group(1)
	search_result = re.search('> *页数[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1:
		base_info['paper_count'] = search_result.group(1)
	search_result = re.search('> *页码[:：]([^<]*) *<', r)
	if search_result is not None and len(search_result.groups()) is 1 and base_info['paper_count'] is not '':
		base_info['paper_count'] = search_result.group(1)
'''

def get_bookname(product_main):
	name_info = product_main.select("div.name_info")
	if len(name_info) != 1:
		return None
	name_info = name_info[0]
	title = name_info.find('h1')
	if title.has_attr('title'):
		return title['title']
	else:
		return None

def getbooks(url)->list:
	"""
	Parameters
	-----------
		url: url for page
	return
	-------
		a list of book
	"""
	# for _ in range(30):
	# 	try:
	# 		r = requests.get(url, timeout=10)
	# 	except requests.exceptions.ConnectionError:
	# 		sleep(10)
	# 		continue
	# 	if r.status_code == 200:
	# 		break
	# if r.status_code != 200:
	# 	return []
	for _ in range(5):
		r = request_url(url)
		if r != None:
			break
	if r == None:
		return []
	# sleep(random.randint(4, 10))

	try:
		categoryPath = re.search(r'(\d\d.){5}\d\d', url).group(0)
	except:
		return []


	soup = BeautifulSoup(r, "html.parser")
	ul = soup.find_all("ul", class_="bigimg")
	if len(ul) == 1:
		# raise Exception(f"length of ul is {len(ul)}")
		ul = ul[0]
	else:
		return []

	items = ul.select('li>a')
	items = list(map(lambda x: x['href'], items))

	# print(items)

	# http://product.dangdang.com/index.php?r=callback%2Fdetail&productId={productId}&templateType=publish&describeMap=&shopId=21144&categoryPath=01.77.28.00.00.00

	# item_url = 'http://product.dangdang.com/1429113915.html'
	books_in_this_page = []
	def getbook(item_url):
		everything_for_this_book = {'shopId': '', 'shop_name': '', 'img_url':'',
		'kaiben':'', 'paper_type':'', 'pack':'', 'ISBN':'', 'is_suit':'', 'book_name':'',
		'publish_time':'','author':'','price':'','weight':'','paper_count':'', 'zhuangzhen':'', 'publisher':''}
		r = request_url(item_url)
		if r is None:
			return None
		# sleep(random.randint(4, 10))
		# get productId
		try:
			productId = re.search(r'(\d+)', item_url).group(0)
		except:
			return None

		soup = BeautifulSoup(r, "html.parser")
		product_main = soup.select('div.product_main.clearfix')
		if len(product_main) != 1:
			return None
		product_main = product_main[0]

		shopinfo = get_shop_info(product_main)
		if shopinfo:
			shopId = shopinfo[0]
		else:
			return None
		everything_for_this_book['shopId'] = shopId
		everything_for_this_book['shop_name'] = shopinfo[1]

		img_url = get_img_url(product_main)
		if img_url is None:
			img_url = ''
		everything_for_this_book['img_url'] = img_url

		book_name = get_bookname(product_main)
		if book_name == None:
			book_name = ''

		messbox_info = get_messbox_info(product_main)

		price = get_price(product_main)

		key_clearfix = soup.select('ul.key.clearfix')
		if len(key_clearfix) == 1:
			key_clearfix = key_clearfix[0]
			clearfix = get_clearfix(key_clearfix)
		else:
			clearfix = None

		base_info = get_base_info(productId, shopId, categoryPath)
		
		if base_info:
			everything_for_this_book.update(base_info)
		if everything_for_this_book['book_name'] =='':
			everything_for_this_book['book_name'] = book_name
		if everything_for_this_book['price'] == '':
			everything_for_this_book['price'] = price if price is not None else ''
		if messbox_info:
			for key in messbox_info:
				if everything_for_this_book[key] == '':
					everything_for_this_book[key] = messbox_info[key]
		if clearfix:
			for key in clearfix:
				if everything_for_this_book[key] == '':
					everything_for_this_book[key] = clearfix[key]
		if everything_for_this_book['ISBN'] == '':
			return None
		print(f'get book: {everything_for_this_book["ISBN"]}')
		return everything_for_this_book

	for item_url in items:
		try:
			everything_for_this_book = getbook(item_url)
			if everything_for_this_book != None:
				books_in_this_page.append(everything_for_this_book)
		except:
			continue
	return books_in_this_page
	# lis = ul.find_all("li")
	# books = []
	# i = 0
	# for li in lis:
		# print(i)
		# i += 1
		# book = []
		# books.append(book)
		# id
		# book.append(li.attrs["id"])
		# lias = li.find_all("a")
		# book name
		# book.append(lias[0].attrs['title'])
		# img url
		# if has_key(lias[0].find("img").attrs, 'data-original'):
			# book.append(lias[0].find("img").attrs['data-original'])
		# else:
			# book.append(lias[0].find("img").attrs['src'])
		# author
		# search_book_author = li.find("p", class_="search_book_author")
		# spans = search_book_author.find_all("span")
		# result = spans[0].find('a')
		# if result is not None:
		# 	book.append(result['title'])
		# else:
			# book.append('')
		# price
		# book.append(li.find('p', class_='price').find('span', class_='search_now_price').text)
	# return books

def cats():
	url = 'http://category.dangdang.com/?ref=www-0-C'
	all_books_cats = {}

	# r = requests.get(url, timeout=10)
	for _ in range(5):
		r = requests.get(url, timeout=10)
		if r.status_code == 200:
			break
	if r.status_code != 200:
		return []

	soup = BeautifulSoup(r.text, "html.parser")
	classify_kinds = soup.find('div', id='floor_1').find_all('div', class_='classify_kind')

	for classify_kind in classify_kinds:
		title = classify_kind.select('.classify_kind_name>a')[0].text
		cats_li = classify_kind.select('ul>li')
		del cats_li[-1]
		cats = {}
		for cat in cats_li:
			a = cat.find('a')
			cats[a.text] = a['href']
			# all_books_cats[a.text] = a['href']
		all_books_cats[title] = cats

	return all_books_cats

def page(link, page):
	if page < 0 or page > 100:
		return None
	return link[:29] + f'pg{page}-' + link[29:]



def thread_func(url, cat, subcat):
	"""
	url like this http://category.dangdang.com/pg2-cp01.03.35.00.00.00.html
	"""
	# this function need modify
	books = []
	cat = cat.replace('/', '-')
	for p in range(1, 2):
		link = page(url, p)
		if link is  None:
			continue
		print(f'getting from cat: {cat}-{subcat}-{link}')
		books += getbooks(link)
	df = pd.DataFrame(books)
	directory = f'./csv/{cat}'
	if not os.path.exists(directory):
		os.makedirs(directory)
	df.to_csv(f'./csv/{cat}/{subcat}.csv', index=False)

def just10page():
	# all_books_cats = cats()
	# threads = []
	file = codecs.open('cats.json', 'r', encoding='unicode_escape')
	cats = json.loads(file.read())
	for cat in cats:
		cat_dir = cats[cat]
		for subcat in cats[cat]:
			# try:
			# 	categoryPath = re.search(r'(\d\d.){5}\d\d', cat_dir[subcat]).group(0)
			# except:
			# 	continue
			thread_func(cat_dir[subcat], cat, subcat)
		# t = threading.Thread(target=thread_func, args=(all_books_cats[key], key))
		# t.start()
		# t.join()
		# threads.append(t)
		# thread_func(all_books_cats[key], key)


	# for t in threads:
	# 	t.join()

if __name__ == '__main__':
	just10page()
