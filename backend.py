import datetime
import e_shop_user as eu
import time
from collections import defaultdict
from constrainfactory import Constrain
from Cache import Cache
from Constants import LIFE_TIME
import log


class frange():
	def __init__(self, left, right):
		self.left = min(left, right)
		self.right = max(left, right)

	def __contains__(self, value):
		return self.left <= value <= self.right


cursor = eu.e_shop_cursor

cache: eu.EShopUser = Cache(LIFE_TIME)

_columns = {}
_category = None


def login(user_id, passwd):
	"""
	:param user_id:
	:param passwd:
	:return: user_name, type(success)
				None, None(failed)
	"""
	if user_id in cache.keys():
		return cache[user_id].user_name, cache[user_id].type
	user = eu.login(user_id, passwd)
	if user:
		cache[user_id] = user
		return user.user_name, user.type
	return None, None


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


def get_books(f, count, price_region=None, subcat=None):
	"""
	:param f: from type int
	:param count: type int
	:param price_region: [low, high], [None, high], [low, None] default None
	:param subcat: subcat in database default None
	:return:list[books] satisfy requirement
	"""
	constrain = Constrain()
	constrain.apply_constraint_value("sub", subcat).apply_constraint_region("price", price_region)
	cursor.execute(f"SELECT * FROM book_info WHERE {constrain}")
	contents = cursor.fetchall()
	t = read_columns("book_info")

	li = [{t[i]: c for i, c in enumerate(content)} for content in contents]
	end = min(len(li), f + count)
	result = li[f:end]
	for content in result:
		if type(content["publish_time"]) == datetime.date:
			content["publish_time"] = content["publish_time"].strftime("%Y-%m-%d")
	return li[f: end]


def userbooklist(username):
	'''
    return [] if failed
    '''
	# return []
	return [{"id": "ppppp", "bookname": "nnnnnn", "imgurl": "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg",
			 "count": "111"}]


# id,bookname,imgurl,price,count


def updateUserBooklist(user_id, operation, isbn, count=None):
	"""
    operation:
        0-insert
        1-update
        2-delete

    return:
        boolean
    """
	now = '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	user: eu.Customer = cache[user_id]
	if operation == 0:
		# do nothing if book already in cart
		# cursor.execute(f'')
		user.add_shopping_cart(isbn, now)
		log.info(f"user {user_id} add book {isbn} to shopping cart")
		pass
	elif operation == 1:
		pass
	elif operation == 2:
		pass

	pass


def history(user_id, isbn, visit_time) -> bool:
	"""
	:param user_id:
	:param isbn:
	:param visit_time:
	:return: True(success) False(failed, maybe login expired)
	"""
	try:
		user: eu.Customer = cache[user_id]
	except KeyError:
		log.debug(f"Cannot find user: {user_id}")
		return False
	user.add_history_record(isbn, visit_time)
	return True


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


def get_book_by_isbn(isbn):
	cursor.execute(f"SELECT * FROM book_info WHERE ISBN='{isbn}'")
	result = cursor.fetchone()
	t = read_columns("book_info")
	if result is not None:
		result = {key: value for key, value in zip(t, result)}
		return result
	else:
		return None
