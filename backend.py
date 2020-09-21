import e_shop_user as eu
import time
from collections import defaultdict
from constrainfactory import Constrain

import log


class frange():
	def __init__(self, left, right):
		self.left = min(left, right)
		self.right = max(left, right)

	def __contains__(self, value):
		return self.left <= value <= self.right


cursor = eu.e_shop_cursor

cache: eu.EShopUser = {}

_columns = {}
_category = None


def login(user_id, passwd):
	"""
	:param user_id:
	:param passwd:
	:return: user_name(success)
				None(failed)
	"""
	if user_id in cache.keys():
		cache[user_id]["time_added"] = time.time()
		return cache[user_id]["user"].user_name
	user = eu.login(user_id, passwd)
	if user:
		cache["user_id"] = {"user": user, "time_added": time.time()}
		return user.user_name
	return None


def get_cats():
	global _category
	if _category is not None:
		return _category
	cursor.execute("SELECT DISTINCT cat, sub FROM book_info")
	cats = cursor.fetchall()
	_category = defaultdict(list)
	for cat_group in cats:
		_category[cat_group[0]].append(cat_group[1])
	return _category


def get_books(f, count, price_region=None, subcat=None):
	constrain = Constrain()
	constrain.apply_constraint_value("sub", subcat).apply_constraint_region("price", price_region)
	cursor.execute(f"SELECT * FROM book_info WHERE {constrain}")
	contents = cursor.fetchall()
	t = read_columns("book_info")

	li = [{t[i]: c for i, c in enumerate(content)} for content in contents]
	end = min(len(li), f + count)
	return li[f: end]


def userbooklist(username):
	'''
    return [] if failed
    '''
	# return []
	return [{"id": "ppppp", "bookname": "nnnnnn", "imgurl": "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg",
			 "count": "111"}]


# id,bookname,imgurl,price,count


def updateUserBooklist(username, operation, **kwargs):
	'''
    operation:
        0-insert
        1-update
        2-delete

    return:
        boolean
    '''

	if operation == 0:
		# do nothing if book already in cart
		# cursor.execute(f'')
		print(f"book {kwargs['id']} add to cart")
		pass
	elif operation == 1:
		pass
	elif operation == 2:
		pass

	pass


def history(username, bookid, time):
	pass


def updateBook(id, author, bookname, imgurl, price):
	cursor.execute(
		f"update book_info set bk_author = '{author}',bk_name = '{bookname}',bk_url = '{imgurl}',bk_price = '{price}' where bk_no = '{id}'")
	cursor.execute(f"select * from book_info where bk_no = '{id}'")
	content = cursor.fetchone()
	t = ['bookname', 'author', 'price', 'type', 'id', 'imgurl']
	obj = {}
	for (i, c) in enumerate(content):
		obj[t[i]] = c
	return obj


def updateBook(id, author, bookname, imgurl, price):
	cursor.execute(
		f"update book_info set bk_author = '{author}',bk_name = '{bookname}',bk_url = '{imgurl}',bk_price = '{price}' where bk_no = '{id}'")
	cursor.execute(f"select * from book_info where bk_no = '{id}'")
	content = cursor.fetchone()
	t = ['bookname', 'author', 'price', 'type', 'id', 'imgurl']
	obj = {}
	for (i, c) in enumerate(content):
		obj[t[i]] = c
	return obj


def read_columns(table_name):
	if table_name in _columns.keys():
		return _columns[table_name]
	cursor.execute(f"DESC {table_name}")
	result = cursor.fetchall()
	result = [content[0] for content in result]
	_columns[table_name] = result
	return result
