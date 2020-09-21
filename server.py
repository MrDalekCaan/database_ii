from socketserver import BaseRequestHandler
from socketserver import TCPServer
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from flask import Flask, render_template, request, redirect, make_response, send_from_directory
import time
import json

# from untitled import books
import backend as B

LIFE_TIME = 60 * 60 * 10


class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		variable_start_string='[[',
		variable_end_string=']]',
	))


app = CustomFlask(__name__, template_folder='.')

# app = Flask(__name__, template_folder='.')
loginpg = 'loginpg.html'
indexpg = './index.html'
managepg = './manage.html'
shoppingcartpg = './shoppingcart.html'
book_infopg = './book_info.html'
registerpg = './register.html'


def readfile(filename):
	file = open(filename, 'r')
	content = file.read()
	return content


def getusername():
	'''
	get username from cookies if there is one
	'''
	return request.cookies.get('username')


def get_user_name():
	return request.cookies.get("user_name")


def updateLogin(resp):
	username = getusername()
	if username:
		resp.set_cookie('username', getusername(), max_age=LIFE_TIME)


def parseParameter(string):
	parameters = string.split('&')
	parameter_set = {}
	for p in parameters:
		p = p.split('=')
		parameter_set[p[0]] = p[-1]
	return parameter_set


@app.route("/")
def root():
	# with open('index.html', 'r') as file:
	# 	html = file.read()
	# return "server response"
	return redirect('/index')


# return html

@app.route('/index')
def index():
	username = getusername()
	# ! need username from backend
	# username = b.getusername(username)
	kwargs = {
		"username": "please login",
		"loginpg": "/loginpg",
		"cart_link": "#",
		"cart": "",
		"history": "",
		"history_link": "",
		"display": "none"
	}
	if username is not None:
		kwargs["loginpg"] = "#"
		kwargs["cart_link"] = "/shoppingcartpg"
		kwargs["cart"] = "购物车"
		kwargs["username"] = username
		kwargs["history"] = "历史记录"
		kwargs["history_link"] = "/historypg"
		kwargs["display"] = ""
	html = render_template(indexpg, **kwargs)
	return html


@app.route("/registerpg")
def registerpage():
	return readfile(registerpg)


@app.route("/register", methods=["POST"])
def register():
	args = parseParameter(request.data.decode('utf-8'))
	username = args['username']
	password = args['password']
	user_id = B.regist(username, password)
	return str(user_id)


@app.route('/cookie/')
def cookie():
	res = make_response("Setting a cookie")
	res.set_cookie('foo', 'bar', max_age=60 * 60 * 24 * 365 * 2)

	# set age to 0 to delete cookie
	# res = make_response("Cookie Removed")
	# res.set_cookie('foo', 'bar', max_age=0)

	# get value of cookie name foo
	# request.cookies.get('foo')
	return res


@app.route('/loginpg')
def loginpage():
	return readfile(loginpg)


@app.route('/manage')
def managepage():
	# return readfile(managepg)
	return render_template(managepg, username='admin')


@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		args = parseParameter(request.data.decode('utf-8'))
		user_id = args['user_id']
		password = args['password']
	else:
		user_id = request.args.get('user_id')
		password = request.args.get('password')

	res = {"state": False}
	user_name = B.login(user_id, password)
	if user_name:
		res["state"] = True
		resp = make_response(json.dumps(res))
		resp.set_cookie("user_name", user_name, max_age=LIFE_TIME)
	else:
		resp = make_response(json.dump(res))
	return resp


@app.route("/cats")
def get_cats():
	return json.dumps(B.get_cats())

@app.route('/books')
def getbooks():
	print(request.args)
	cat = request.args.get('cat')
	f = int(request.args.get('from'))
	count = int(request.args.get('count'))
	low = request.args.get('low')
	high = request.args.get('high')
	if low == 'null':
		low = None
	else:
		low = int(request.args.get('low'))
	if high == 'null':
		high = None
	else:
		high = int(request.args.get('high'))
	bks = B.findBookList(cat, f, count, low, high)
	# bks = books(cat, f, count, low, high)
	bks = {"content": bks}

	return json.dumps(bks)


# return '''
# {
# 	"content":[{"name":"幼儿绘本", "price":"¥29.70", "image":"http://img3m4.ddimg.cn/58/18/1179371614-1_b_14.jpg", "author":""},
# 	 {"name":"全5册早教书籍", "price":"¥29.80", "image":"http://img3m4.ddimg.cn/37/3/1202388004-1_b_2.jpg", "author":""},
# 	 {"name":"幼儿绘本", "price":"¥29.70", "image":"http://img3m4.ddimg.cn/58/18/1179371614-1_b_14.jpg", "author":""}]
# }
# '''

@app.route('/book')
def getbook():
	return '''
	{
		"content": [{"name":"幼儿绘本", "price":"¥29.70", "image":"http://img3m4.ddimg.cn/58/18/1179371614-1_b_14.jpg", "author":""}]
	}
	'''


def padzero(t):
	t = str(t)
	return t if len(t) == 2 else f'0{t}'


@app.route("/book_info")
def bookInfo():
	username = getusername()
	bookid = request.args.get("id")
	book = B.getBookById(bookid)
	t = time.gmtime()
	if username:
		B.history(username, bookid,
				  f'{t.tm_year}{padzero(t.tm_mon)}{padzero(t.tm_mday)}{padzero((t.tm_hour + 8) % 24)}{padzero(t.tm_min)}{padzero(t.tm_sec)}')
	resp = make_response(render_template(book_infopg, **book))
	updateLogin(resp)
	return resp


# ----------manager------------
def change(**kw):
	return kw


def deleteById(bookid):
	"""
	delete entry by id

	return:
		true(success), false(failed)
	"""
	try:
		# delete book
		pass
	except Exception as e:
		return False
	return True


@app.route('/manage/change', methods=["POST"])
def manageChange():
	"""
	change entry in database

	return:
		changed entry -> json string
	"""
	args = parseParameter(request.data.decode("utf-8"))
	# ! change is function by wzy
	result = change(**args)
	result = {"content": result}
	return json.dumps(result)


@app.route("/manage/delete", methods=["POST"])
def manageDelete():
	args = parseParameter(request.data.decode("utf-8"))
	result = deleteById(args["id"])
	if result:
		return "1"
	return "0"


# --------------user-------------
@app.route("/addToCart")
def addToCart():
	username = getusername()
	id = request.args.get("id")
	B.updateUserBooklist(username, 0, id, 1)
	return '0'


@app.route("/shoppingcartpg")
def shoppingcartpg():
	username = getusername()
	if username is None:
		return redirect("/loginpg")
	resp = render_template("shoppingcart.html", username=username, loginpg='#', cart_history="shoppingcart")
	resp = make_response(resp)
	updateLogin(resp)
	return resp


@app.route("/historypg")
def historypg():
	username = getusername()
	if username is None:
		return redirect("/loginpg")
	resp = render_template("shoppingcart.html", username=username, loginpg='#', cart_history="history")
	resp = make_response(resp)
	updateLogin(resp)
	return resp


@app.route('/history')
def history():
	username = getusername()
	content = B.getVisitlogs(username)
	return json.dumps({"content": content})


@app.route("/shoppingcart")
def shoppingcart():
	username = getusername()
	if not username:
		return redirect("/loginpg")

	# res = b.userbooklist(username)
	res = [{'bookname': "nnnnnn",
			'count': "222",
			'id': "ppppp",
			'imgurl': "http://img3m3.ddimg.cn/51/25/23977653-1_b_12.jpg"}]

	res = {"content": res}
	resp = make_response(json.dumps(res))
	updateLogin(resp)
	return resp


@app.route("/shoppingcartChange")
def changenum():
	username = getusername()
	if username is None:
		return redirect("/loginpg")
	id = request.args.get("id")
	num = request.args.get("num")
	if num == '0' or num == 0:
		B.updateUserBooklist(username, 2, id)
	else:
		B.updateUserBooklist(username, 1, id, num)

	content = {"content": []}
	return json.dumps(content)


# static file
@app.route('/css/<path:path>')
def css(path):
	return send_from_directory('css', path)


@app.route('/img/<path:path>')
def img(path):
	return send_from_directory('img', path)


@app.route('/js/<path:path>')
def js(path):
	return send_from_directory('js', path)


@app.errorhandler(404)
def err404(e):
	return redirect('/')


class TCPHandler(BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(4096).strip()
		print(self.data)
		self.request.sendall(b"server response")
# or use this: self.wfile.write(b"server response")


class httphander(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/':
			self.path = "index.html"
			self.send_response(200)
		else:
			self.send_response(404)
		self.end_headers()
		self.wfile.write(bytes("server response", "utf-8"))


# def do_POST


if __name__ == "__main__":
	host, port = "0.0.0.0", 5001

	# with TCPServer((host, port), TCPHandler) as server:
	# 	server.serve_forever()

	# server = HTTPServer((host, port), httphander)
	# server.serve_forever()

	# with HTTPServer((host, port), httphander) as server:
	# 	server.serve_forever()

	app.run(host, port)
