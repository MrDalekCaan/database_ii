from socketserver import BaseRequestHandler
from socketserver import TCPServer
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from flask import Flask, render_template, request, redirect, make_response, send_from_directory
import time
import datetime
import json
import os
from Constants import LIFE_TIME, FAIL, OK
# from untitled import books
import backend as B
import log


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
book_info_page_path = './book_info.html'
register_page_path = './register.html'
mobile_login_page_path = "./m.html"


def readfile(filename):
	file = open(filename, 'r')
	content = file.read()
	return content


def get_user_id():
	"""
	get username from cookies if there is one
	"""
	return request.cookies.get('user_id')


def get_user_name():
	return request.cookies.get("user_name")


def get_user_type():
	return request.cookies.get("user_type")


def update_login(resp):
	user_id = get_user_id()
	if user_id:
		resp.set_cookie('user_id', get_user_id(), max_age=LIFE_TIME)
		resp.set_cookie('user_name', get_user_name(), max_age=LIFE_TIME)
		resp.set_cookie('user_type', get_user_type(), max_age=LIFE_TIME)


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
	user_id = get_user_id()
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
	if user_id is not None:
		kwargs["loginpg"] = "#"
		kwargs["cart_link"] = "/shoppingcartpg"
		kwargs["cart"] = "购物车"
		kwargs["username"] = get_user_name()
		kwargs["history"] = "历史记录"
		kwargs["history_link"] = "/historypg"
		kwargs["display"] = ""
	html = render_template(indexpg, **kwargs)
	return html


@app.route("/registerpg")
def registerpage():
	return readfile(register_page_path)


@app.route("/register", methods=["POST"])
def register():
	args = parseParameter(request.data.decode('utf-8'))
	username = args['username']
	password = args['password']
	user_id = B.register(username, password)
	return json.dumps({"user_id": user_id})


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


@app.route('/manage')
def managepage():
	# return readfile(managepg)
	return render_template(managepg, username='admin')


@app.route('/loginpg')
def loginpage():
	token = B.generate_login_token()
	img_url = B.generate_qr_by_token(token)
	resp = make_response(render_template(loginpg, img_url=img_url))
	resp.set_cookie("token", token)
	return resp


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
	user_name, user_type = B.login(user_id, password)
	if user_name:
		res["state"] = True
		resp = make_response(json.dumps(res))
		resp.set_cookie("user_name", user_name, max_age=LIFE_TIME)
		resp.set_cookie("user_id", user_id, max_age=LIFE_TIME)
		resp.set_cookie("user_type", user_type, max_age=LIFE_TIME)
	else:
		resp = make_response(json.dumps(res))
	return resp


@app.route("/login_state")
def login_state():
	"""
	error:
	0. normal
	1. token expired
	"""
	token = request.cookies.get("token")
	status = {"login_state": False, "error": 0, "user_info": None}
	try:
		if B.token_cache[token]:
			status["user_info"] = B.token_cache[token]
			status["login_state"] = True
		else:
			pass
	except KeyError:
		status["error"] = 1
	finally:
		return json.dumps(status)


@app.route("/mobile_login", methods=['POST'])
def mobile_login():
	token = request.cookies.get("token")
	args = parseParameter(request.data.decode("utf-8"))
	user_id = args["user_id"]
	password = args["password"]
	if B.mobile_login(token, user_id, password):
		return OK
	else:
		return FAIL


@app.route("/mobile_login_page")
def mobile_login_page():
	token = request.args.get("token")
	resp = make_response(readfile(mobile_login_page_path))
	resp.set_cookie("token", token)
	return resp


@app.route("/cats")
def get_cats():
	return json.dumps(B._get_cats())


@app.route('/books')
def get_books():
	log.debug(request.args)
	subcat = request.args.get('subcat')
	f = int(request.args.get('from'))
	count = int(request.args.get('count'))
	low = null_parameter(request.args.get('low'))
	high = null_parameter(request.args.get('high'))
	key_word = null_parameter(request.args.get('key_word'))
	order = request.args.get('orderby')
	bks = B.get_books(f, count, price_region=[low, high], subcat=subcat, key_word=key_word, order=order)
	bks = {"content": bks}
	return json.dumps(bks)


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
def get_book_info():
	"""
	When user call this function, a browser history will record
	"""
	user_id = get_user_id()
	isbn = request.args.get("isbn")
	book = B.get_book_by_isbn(isbn)
	if user_id:
		B.add_history_record(user_id, isbn, '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now()))
	resp = make_response(render_template(book_info_page_path, **book))
	update_login(resp)
	return resp


# ----------manager-----------
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
def add_to_cart():
	user_id = get_user_id()
	isbn = request.args.get("isbn")
	if B.update_user_cart(user_id, 0, isbn, 1):
		return OK
	return FAIL


@app.route("/shoppingcartpg")
def shoppingcartpg():
	username = get_user_id()
	if username is None:
		return redirect("/loginpg")
	resp = render_template("shoppingcart.html", username=username, loginpg='#', cart_history="shoppingcart")
	resp = make_response(resp)
	update_login(resp)
	return resp


@app.route("/historypg")
def historypg():
	user_id = get_user_id()
	if user_id is None:
		return redirect("/loginpg")
	user_name = get_user_name()
	resp = render_template("shoppingcart.html", username=user_name, loginpg='#', cart_history="history")
	resp = make_response(resp)
	update_login(resp)
	return resp


@app.route('/history')
def history():
	user_id = get_user_id()
	content = B.get_visit_history(user_id)
	return json.dumps({"content": content})


@app.route("/shoppingcart")
def shoppingcart():
	user_id = get_user_id()
	if not user_id:
		return redirect("/loginpg")
	res = B.get_user_cart(user_id)
	res = {"content": res}
	resp = make_response(json.dumps(res))
	update_login(resp)
	return resp


@app.route("/shoppingcart/change")
def changenum():
	user_id = get_user_id()
	if user_id is None:
		return redirect("/loginpg")
	isbn = request.args.get("isbn")
	num = request.args.get("num")
	# if num == '0' or num == 0:
	# 	B.update_user_cart(user_id, 1, isbn)
	# else:
	# 	B.update_user_cart(user_id, 1, isbn, num)
	B.update_user_cart(user_id, 1, isbn, num)
	# content = {"content": []}
	# return json.dumps(content)
	return "OK"


@app.route("/purchase")
def purchase():
	user_id = get_user_id()
	if not user_id:
		return FAIL
	isbn = request.args.get('isbn')
	count = request.args.get('count')
	if B.purchase(user_id, isbn, count):
		return OK
	return FAIL


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


def null_parameter(value):
	return None if value == '' or value is None or value.lower() == 'null' else value


if __name__ == "__main__":
	host, port = "0.0.0.0", 5001

	for img in os.listdir('./img/token'):
		os.remove(os.path.join('./img/token', img))

	# with TCPServer((host, port), TCPHandler) as server:
	# 	server.serve_forever()

	# server = HTTPServer((host, port), httphander)
	# server.serve_forever()

	# with HTTPServer((host, port), httphander) as server:
	# 	server.serve_forever()

	app.run(host, port)
