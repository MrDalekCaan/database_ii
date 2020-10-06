import datetime

import e_shop_user as eu
import time
from collections import defaultdict
from constrainfactory import Constrain
from Cache import Cache
from Constants import CACHE_TIME, SERVER_PORT, TOKEN
import log
import qrcode
import socket
import string
import random
import pandas as pd


class frange():
	def __init__(self, left, right):
		self.left = min(left, right)
		self.right = max(left, right)
				
	def __contains__(self, value):
		return self.left <= value <= self.right


cursor = eu.e_shop_cursor

user_cache = Cache(CACHE_TIME)
column_cache = {}
token_cache = Cache(TOKEN)
""":content {user_id user_name user_type} | None"""
_columns = {}
_category = None


def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]


def generate_login_token():
	letters = string.ascii_uppercase
	return ''.join(random.choice(letters) for i in range(20))


def generate_qr_by_token(token):
	img_url = f"http://{get_ip_address()}:{SERVER_PORT}/img/token/{token}.png"
	img_content = f"http://{get_ip_address()}:{SERVER_PORT}/mobile_login_page?token={token}"
	img = qrcode.make(img_content)
	with open(f"./img/token/{token}.png", "wb") as file:
		img.save(file, "png")
	token_cache[token] = None
	return img_url


def mobile_login(token, user_id, password):
	user_name, user_type = login(user_id, password)
	if user_name:
		token_cache[token] = {"user_name": user_name, "user_id": user_id, "user_type": user_type}
		return token_cache[token]
	else:
		return None


def login(user_id, passwd):
	"""
	:param user_id:
	:param passwd:
	:return: user_name, type(success)
				None, None(failed)
	"""
	if user_id in user_cache.keys():
		return user_cache[user_id].user_name, user_cache[user_id].type
	user = eu.login(user_id, passwd)
	if user:
		user_cache[user_id] = user
		return user.user_name, user.type
	return None, None


def register(username, password):
	return eu.register(username, password)


def _get_cats():
	global _category
	if _category is not None:
		return _category
	cursor.execute("SELECT DISTINCT cat, sub FROM book_info")
	cats = cursor.fetchall()
	_category = defaultdict(list)
	for cat_group in cats:
		_category[cat_group[0]].append(cat_group[1])
	return _category


def get_books(f, count, price_region=None, subcat=None, key_word=None, order=None):
	"""
	:param key_word: use for fuzzy search
	:param f: from type int
	:param count: type int
	:param price_region: [low, high], [None, high], [low, None] default None
	:param subcat: subcat in database default None
	:return:list[books] satisfy requirement
	"""
	switch = {'time_desc': ("publish_time", "DESC"),
			  'time_asc': ("publish_time", "ASC"),
			  'sold_asc': ("sold_count", 'ASC'),
			  'sold_desc': ("sold_count", 'DESC')}
	(order_property, order_way) = switch[order]
	constrain = Constrain()
	log.debug(f"get_books-price_region:{price_region}")
	constrain.apply_constraint_value("sub", subcat).apply_constraint_region("price", price_region). \
		like(["book_name", "cat", "sub", "author", "ISBN"], f"%{key_word}%").order_by(order_property, order_way).from_(f).limit(count)
	log.debug(constrain)
	cursor.execute(f"SELECT * FROM book_info {constrain}")
	contents = cursor.fetchall()
	t = read_columns(cursor, "book_info")
	li = [{t[i]: c for i, c in enumerate(content)} for content in contents]
	return [date_time_toString("publish_time", content) for content in li]


def get_personal_recommendation(user_id, f, count, price_region=None, subcat=None, key_word=None):
	# constrain = Constrain()
	# cursor.execute(f"""
	# SELECT *
	# FROM book_info
	# LEFT JOIN
	# (SELECT isbn  FROM customer_{user_id}.browser_history) B
	# ON
	# book_info.isbn=B.isbn
	# GROUP BY book_info.isbn
	# ORDER BY  COUNT(B.isbn) DESC
	# LIMIT {f}, {count}
	# """)
	user = _get_user(user_id)
	isbn_order_by_view_count = user.get_view_count()
	books = []
	d = defaultdict(int)
	for pack in isbn_order_by_view_count:
		isbn = pack[0]
		view_count = pack[1]
		cursor.execute(f"SELECT sub FROM book_info WHERE ISBN={isbn}")
		result = cursor.fetchone()
		d[result[0]] += view_count
		# books.append(result)
	max_view_count = max([d[key] for key in d])
	subs = []
	for key in d:
		if d[key] == max_view_count:
			subs.append(key)
	log.debug(f"Personal recommendation category: {subs}")

	# li = [{t[i]: c for i, c in enumerate(content)} for content in books]
	# li = [date_time_toString("publish_time", content) for content in li]
	# end here get max sub
	# log.debug(f"{d}")
	# log.debug(f"{subs}")
	# log.debug(f"{Constrain().apply_constraint_value('sub', subs)}")
	constraints = Constrain()
	constraints.apply_constraint_value('sub', subs).apply_constraint_region("price", price_region).\
		order_by("sold_count").from_(f).limit(count)
	cursor.execute(f"SELECT * FROM book_info {constraints}")
	books = cursor.fetchall()
	columns = read_columns(cursor, "book_info")
	li = [{columns[i]: c for i, c in enumerate(content)} for content in books]
	li = [date_time_toString("publish_time", content) for content in li]
	return li
	# dataframe = pd.DataFrame(li)
	# return dataframe


def get_user_cart(user_id):
	"""
    return [] if failed
    """
	user = _get_user(user_id)
	contents = user.get_shopping_cart()
	t = read_columns(user.cursor, "shopping_cart")
	li = [{t[i]: c for i, c in enumerate(content)} for content in contents]
	return [date_time_toString("time", book_info) for book_info in li]


def update_user_cart(user_id, operation, isbn, count=None):
	"""
	:param count:
	:param isbn:
	:param user_id:
	:param operation: 0 delete
	 							1 update
    """
	now = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	# user: eu.Customer = user_cache[user_id]
	user: eu.Customer = _get_user(user_id)
	if operation == 0:
		if user.add_shopping_cart(isbn, now):
			log.info(f"user {user_id} add book {isbn} to shopping cart")
			return True
		log.fatal(f"user {user_id} add book {isbn} to shopping cart failed")
		return False
	elif operation == 1:
		if user.update_shopping_cart(isbn, count):
			log.info(f"user {user_id} update book {isbn} to {count}")
			return True
		log.fatal(f"user {user_id} update book {isbn} to {count} failed")
		return False


def add_history_record(user_id, isbn, visit_time) -> bool:
	"""
	add history record
	:param user_id:
	:param isbn:
	:param visit_time:
	:return: True(success) False(failed, maybe login expired)
	"""
	try:
		user: eu.Customer = user_cache[user_id]
	except KeyError:
		log.debug(f"Cannot find user: {user_id}")
		return False
	user.add_history_record(isbn, visit_time)
	return True


def change_book_info(user_id, kwargs):
	user = _get_user(user_id)
	log.debug(kwargs)
	log.debug(user.type)
	return user.change_book_info(kwargs)


def read_columns(cursor, table_name: str):
	key = hex(id(cursor)) + table_name
	# if table_name in _columns.keys():
	# 	return _columns[table_name]
	if key in column_cache.keys():
		return column_cache[key]
	cursor.execute(f"DESC {table_name}")
	result = cursor.fetchall()
	result = [content[0] for content in result]
	# _columns[table_name] = result
	column_cache[key] = result
	return result


def get_book_by_isbn(isbn):
	"""
	:param isbn:
	:return: dict
	"""
	cursor.execute(f"SELECT * FROM book_info WHERE ISBN='{isbn}'")
	result = cursor.fetchone()
	t = read_columns(cursor, "book_info")
	if result is not None:
		result = {key: value for key, value in zip(t, result)}
		return date_time_toString("publish_time", result)
	else:
		return None


def get_visit_history(user_id):
	user = _get_user(user_id)
	contents = user.get_history_record()
	t = read_columns(user.cursor, "browser_history")
	li = [{t[i]: c for i, c in enumerate(content)} for content in contents]
	return [date_time_toString('time', content) for content in li]


def purchase(user_id, isbn, count):
	user = _get_user(user_id)
	purchase_time = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	return user.purchase(isbn, purchase_time, count)


def date_time_toString(property_name, book_info):
	try:
		book_info[property_name] = book_info[property_name].strftime("%Y-%m-%d %H:%M:%S")
	except:
		pass
	finally:
		return book_info


def _get_user(user_id):
	try:
		user = user_cache[user_id]
	except KeyError:
		user = eu.get_user(user_id)
		user_cache[user_id] = user
	return user
