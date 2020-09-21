import pandas as pd
import re
import mysql.connector
import log
import os

dbconfig = {'host': '127.0.0.1',
				'user': 'root',
				'password': '734660',
				'database': 'book_e_shop'}

try:
	conn = mysql.connector.connect(**dbconfig)
except mysql.connector.errors.ProgrammingError as e:
	if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
		conn = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'])
		cursor = conn.cursor()
		cursor.execute(f"CREATE DATABASE {dbconfig['database']}")
		conn = mysql.connector.connect(**dbconfig)

cursor = conn.cursor()


def correctify_datetime(time):
	times = time.split('-')
	if len(times) >= 1 and times[0].isdigit():
		year = times[0]
	else:
		year = '0000'
	if len(times) >= 2 and times[1].isdigit():
		month = times[1]
	else:
		month = '01'
	if len(times) >= 3 and times[2].isdigit():
		day = times[2]
	else:
		day = '01'
	return f'{year}-{month}-{day}'


def use_database(database_name):
	try:
		cursor.execute(f"use {database_name}")
	except mysql.connector.errors.ProgrammingError as e:
		return False
	return True


def create_database(database_name):
	# mysql.connector.errorcode.ER_DB_CREATE_EXISTS
	try:
		cursor.execute(f"CREATE DATABASE {database_name}")
	except mysql.connector.errors.ProgrammingError as e:
		return False
	return True


def create_table(table_name, definition):
	cursor.execute(f"CREATE TABLE {table_name} ({definition})")


def build_data(cat, csv_filename) -> str:
	subcat = csv_filename.split('/')[-1]
	subcat = subcat.split('.')[0]
	df = pd.read_csv(csv_filename)
	df.fillna('', inplace=True)
	df.loc[:, 'ISBN'] = df.loc[:, 'ISBN'].astype('str')
	digit = ~df.loc[:, 'ISBN'].str.isdigit()
	def lam(isbn):
		return re.sub(r'[^0-9]', '', isbn)
	df.loc[digit, 'ISBN'] = df.loc[digit, 'ISBN'].apply(lam)
	df.loc[:, 'publish_time'] = df.loc[:, 'publish_time'].apply(correctify_datetime)
	digit = df.loc[:, 'ISBN'].str.isdigit()
	df = df.loc[digit, :].reset_index(drop=True)
	df['is_suit'].where(df['is_suit'] == '是', other='0', inplace=True)
	df['is_suit'].where(df['is_suit'] == '0', other='1', inplace=True)
	df.drop_duplicates(subset='ISBN', inplace=True)

	def to_string(row):
		string = ""
		for content in row:
			string += f"'{content}', "
		string += f"'{cat}', '{subcat}', "
		string = string.strip(' ,')
		string = f"({string}), "
		return string

	data = ""
	for row in df.apply(to_string, axis=1):
		data += row
	data = data.strip(' ,')
	column_name = ""
	for column in df._columns:
		column_name += f"{column},"
	column_name += f"cat, sub"
	column_name = f"({column_name.strip(' ,')})"
	return f"{column_name} VALUES {data}"


def insert_into(table_name, data):
	try:
		cursor.execute(f"INSERT INTO  {table_name} {data}")
		conn.commit()
	except mysql.connector.errors.IntegrityError as e:
		# if e.errno == 1062:
		log.fatal(e.msg)


def alter_column(table, column, definition):
	cursor.execute(f"ALTER TABLE {table} MODIFY {column} {definition}")


def build_book_e_shop():
	definition = """
	shopId VARCHAR(10),
	shop_name VARCHAR(40),
	img_url VARCHAR(400),
	kaiben VARCHAR(10),
	paper_type VARCHAR(10),
	pack VARCHAR(10),
	ISBN VARCHAR(20) PRIMARY KEY,
	is_suit CHAR(1),
	book_name VARCHAR(400),
	publish_time DATE,
	author VARCHAR(400),
	price VARCHAR(10),
	weight VARCHAR(10),
	paper_count VARCHAR(10),
	zhuangzhen VARCHAR(10),
	publisher VARCHAR(400),
	cat VARCHAR(10),
	sub VARCHAR(10)
	"""
	create_table('book_info', definition)

	definition = '''
	user_name VARCHAR(32),
	user_id VARCHAR(20) PRIMARY KEY NOT NULL,
	password VARCHAR(24),
	type CHAR(4)
	'''
	create_table('user', definition)

	definition = '''
	ISBN VARCHAR(20),
	inventory INT,
	FOREIGN KEY (ISBN) REFERENCES book_info(ISBN)
	'''
	create_table('storage', definition)

	definition = '''
	ISBN VARCHAR(20),
	count INT,
	time DATETIME,
	FOREIGN KEY(ISBN) REFERENCES book_info(ISBN)
	'''
	create_table('shopping_history', definition)


def main():
	build_book_e_shop()
	cats = os.listdir('./csv')
	cats.remove('.DS_Store')
	for catdir in cats:
		for subcat in os.listdir(os.path.join('./csv', catdir)):
			path = os.path.join('./csv', catdir, subcat)
			data = build_data(catdir, path)
			insert_into('book_info', data)


if __name__ == '__main__':
	main()
