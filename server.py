from socketserver import BaseRequestHandler
from socketserver import TCPServer
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from flask import Flask, render_template, request, redirect, make_response, send_from_directory, render_template
import json

from untitled import books


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
managepg= './manage.html'

def readfile(filename):
	file = open(filename, 'r')
	content = file.read()
	return content

def getusername():
	return request.cookies.get('username')

def updateLogin(resp):
	resp.set_cookie('username', getusername(), max_age=6*10)

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
	if username is not None:
		html = render_template(indexpg, username=username, loginpg='#')
	else:
		html = render_template(indexpg, username='please login', loginpg='/loginpg')
	return html

@app.route('/cookie/')
def cookie():
    res = make_response("Setting a cookie")
    res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)

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

def varifyuser(username, password):
	if username == 'admin' and password == 'p':
		return True
	return False



@app.route("/login", methods=['GET', 'POST'])
def login():
	# print(f'login request method {request.method}')
	# print(request.data)
	# if request.cookies.get('username'):
		# resp = make_response(f'hello {getusername()}')
		# resp = make_response('/')
		# updateLogin(resp)
		# return resp 
		# already login
		# goto user's page

	# username = request.args.get('username')
	if request.method == 'POST':
		args = parseParameter(request.data.decode('utf-8'))
		username = args['username']
		password = args['password']
	else:
		username = request.args.get('username')	
		password = request.args.get('password')

	#! varifyuser by wzy
	if varifyuser(username, password):
		# res = make_response('this is a html file')
		# resp = redirect('/index')
		resp = make_response('/')
		resp.set_cookie('username', username, max_age=60*10)		# 10 minutes
	else:
		resp = make_response('0')

	return resp

@app.route('/books')
def getbooks():
	cat = request.args.get('cat')
	f = int(request.args.get('from'))
	count = int(request.args.get('count'))
	bks = books(cat, f, count)
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
	#! change is function by wzy
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





