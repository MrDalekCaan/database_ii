import mysql.connector
import time
import log

dbconfig = {
	'host': "localhost",
	'user': "root",
	'passwd': "734660",
	'database': "book_e_shop",
}
book_e_shop = mysql.connector.connect(**dbconfig)
e_shop_cursor = book_e_shop.cursor()


class EShopUser:
	def __new__(cls, *args, **kwargs):
		if cls is EShopUser:
			raise TypeError("base class may not be instantiated")
		return super(EShopUser, cls).__new__(cls)

	def __init__(self, user_id, user_name):
		self._user_id = user_id
		self._user_name = user_name
		self.db = None
		self.cursor = None

	@property
	def user_id(self):
		return self._user_id

	@property
	def user_name(self):
		return self._user_name

	def database_name(self):
		if self.cursor is None:
			return ""
		database_name = ""
		try:
			self.cursor.execute("SELECT DATABASE()")
			database_name = self.cursor.fetchone()[0]
		except Exception as e:
			log.warn(e)
		return database_name

	def delete_tables(self) -> bool:
		"""
		delete all tables in users database
		:return: True(success), False(failed)
		"""
		if self.cursor is None:
			return False
		self.cursor.execute(f"SHOW TABLES")
		tables = [content[0] for content in self.cursor.fetchall()]
		if len(tables) == 0:
			return True
		table_names = ""
		for table_name in tables:
			table_names += f"{table_name}, "
		table_names = table_names.strip(', ')
		log.info(f"delete tables: {table_names} from database: {self.database_name()}")
		self.cursor.execute(f"DROP TABLES IF EXISTS {table_names}")
		return True

	def create_table(self, table_name, definition) -> bool:
		"""
		:param table_name:
		:param definition:
		:return: True(success), False(failed)
		"""
		try:
			self.cursor.execute(f"CREATE TABLE {table_name} ({definition})")
		except mysql.connector.errors.ProgrammingError as e:
			log.fatal(f"Create table failed: {e.msg}")
			return False
		return True

	@staticmethod
	def get_database(dbconfig: dict):
		try:
			db = mysql.connector.connect(**dbconfig)
		except mysql.connector.errors.ProgrammingError as e:
			if e.errno == 1049:
				log.warn(e.msg)
				log.info(f"Trying to create new database: {dbconfig['database']}")
				db = mysql.connector.connect(host=dbconfig['host'],
											 user=dbconfig['user'],
											 passwd=dbconfig['passwd'])
				cursor = db.cursor()
				cursor.execute(f"CREATE DATABASE {dbconfig['database']}")
				db = mysql.connector.connect(**dbconfig)
				return db, db.cursor()
		return db, db.cursor()


class Customer(EShopUser):
	type = '0001'

	def __init__(self, user_id, user_name):
		super(Customer, self).__init__(user_id, user_name)
		config = dbconfig.copy()
		config["database"] = f"customer_{user_id}"
		self.db, self.cursor = self.get_database(config)
		# check table
		self.cursor.execute("SHOW TABLES")
		tables = self.cursor.fetchall()
		tables = [content[0] for content in tables]
		if "shopping_cart" not in tables or "browser_history" not in tables or "purchase_history" not in tables:
			log.warn(f"Get table {tables}, should get table: shopping_cart, browser_history, purchase_history")
			log.info(f"Recreating tables: shopping_cart, browser_history, purchase_history")
			self.recreate_table()
		# check end

	def recreate_table(self):
		self.delete_tables()
		definition = '''
		ISBN VARCHAR(20) PRIMARY KEY NOT NULL,	
		count INT,
		time DATETIME,
		FOREIGN KEY (ISBN) REFERENCES book_e_shop.book_info(ISBN) 
		'''
		self.create_table("shopping_cart", definition)

		definition = '''
		ISBN VARCHAR(20) NOT NULL,
		time DATETIME,
		FOREIGN KEY (ISBN) REFERENCES book_e_shop.book_info(ISBN)	
		'''
		self.create_table("browser_history", definition)

		definition = '''
		ISBN VARCHAR(20) NOT NULL,	
		time DATETIME, 
		count INT,
		FOREIGN KEY (ISBN) REFERENCES book_e_shop.book_info(ISBN)	
		'''
		self.create_table("purchase_history", definition)

	def add_history_record(self, isbn, visit_time):
		self.cursor.execute(f"INSERT INTO browser_history(ISBN, time) VALUES ({isbn}, {visit_time})")
		self.db.commit()

	def add_shopping_cart(self, isbn, add_time):
		try:
			self.cursor.execute(f"INSERT INTO shopping_cart(isbn, count, time) VALUES ({isbn}, 1, {add_time})")
		except mysql.connector.errors.IntegrityError:
			self.cursor.execute(f"SELECT count FROM shopping_cart WHERE ISBN='{isbn}'")
			count = self.cursor.fetchone()[0]
			self.cursor.execute(f"UPDATE shopping_cart SET count={count + 1} WHERE ISBN='{isbn}'")
		finally:
			self.db.commit()

	def get_shopping_cart(self):
		self.cursor.execute(f"SELECT * FROM shopping_cart ORDER BY time DESC")
		result = self.cursor.fetchall()
		# TODO: HERE
		pass


class Admin(EShopUser):
	type = '0000'

	def __init__(self, user_id, user_name):
		super(Admin, self).__init__(user_id, user_name)
		config = dbconfig.copy()
		config["database"] = f"admin_{user_id}"
		self.db, self.cursor = self.get_database(config)
		self.cursor.execute(f"SHOW TABLES")
		# check table
		tables = self.cursor.fetchall()
		if len(tables) != 1:
			log.warn(f"Get table {tables}, should get table: change_history")
			log.info(f"Recreating table: change_history")
			self.recreate_table()
		elif tables[0][0] != 'change_history':
			log.warn(f"Get table {tables}, should get table: change_history")
			log.info(f"Recreating table: change_history")
			self.recreate_table()

	# end check

	def recreate_table(self):
		self.delete_tables()
		definition = '''
		ISBN VARCHAR(20) NOT NULL,
		property VARCHAR(15),
		new_value VARCHAR(400),
		old_value VARCHAR(400),
		time TIMESTAMP,
		FOREIGN KEY (ISBN) REFERENCES book_e_shop.book_info(ISBN)
		'''
		self.create_table('change_history', definition)


def login(user_id, password):
	"""
	:param user_id:
	:param password:
	:return: None(login failed) EShopUser(login success)
	"""
	password = str(password)
	e_shop_cursor.execute(f"SELECT * FROM user WHERE user_id = '{user_id}'")
	user_info = e_shop_cursor.fetchone()
	if user_info is None:
		return None
	if password != user_info[2]:
		return None
	if user_info[3] == '0000':
		return Admin(user_info[1], user_info[0])
	elif user_info[3] == '0001':
		return Customer(user_info[1], user_info[0])


def register(user_name, password):
	user_id = int(abs(hash(f"{user_name}{time.time()}")) % 1e7)
	while True:
		e_shop_cursor.execute(f"SELECT user_id FROM user WHERE user_id={user_id}")
		if not e_shop_cursor.fetchone():
			break
		user_id = int(abs(hash(f"{user_name}{time.time()}")) % 1e7)
	e_shop_cursor.execute(f"""INSERT INTO user(user_name, user_id, password, type) VALUES 
														('{user_name}', '{user_id}', '{password}', '0001')""")
	book_e_shop.commit()
	return user_id


'''
import e_shop_user as e
from importlib import reload
'''
