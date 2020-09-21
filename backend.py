import mysql.connector
import e_shop_user as eu
import time
from collections import defaultdict


class frange():
	def __init__(self, left, right):
		self.left = min(left, right)
		self.right = max(left, right)

	def __contains__(self, value):
		return self.left <= value <= self.right


cursor = eu.e_shop_cursor

cache: eu.EShopUser = {}


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
	cursor.execute("SELECT DISTINCT cat, sub FROM book_info")
	cats = cursor.fetchall()
	cat_sub = defaultdict(list)
	for cat_group in cats:
		cat_sub[cat_group[0]].append(cat_group[1])
	return cat_sub

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


def findBookList(cat, f, count, low=None, high=None):
	print(f"select * from book_info where bk_type = {cat}")
	cursor.execute(f"select * from book_info where bk_type = '{cat}'")
	contents = cursor.fetchall()

	# contents = contents[f:f+count]
	def lam(e):
		ee = list(e)
		try:
			ee[2] = float(e[2].split('¥')[-1])
		except Exception as error:
			ee[2] = 0
		return ee

	contents = list(map(lam, contents))
	# remove el not in [low, high]
	if low is not None and high is not None:
		fr = frange(low, high)
		for i in reversed(range(len(contents))):
			if contents[i][2] not in fr:
				contents.pop(i)

	t = ['bookname', 'author', 'price', 'type', 'id', 'imgurl']
	li = [{t[i]: c for i, c in enumerate(content)} for content in contents]
	end = min(len(li), f + count)
	return li[f: end]


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

# User1 = User()
