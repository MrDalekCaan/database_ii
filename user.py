import mysql.connector


dbconfig = {'host': '127.0.0.1',
    'user': 'root',
    'password': '734660',
    'database': 'users'}
try:
    conn = mysql.connector.connect(**dbconfig)
except mysql.connector.errors.ProgrammingError as e:
    if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        conn = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['user'], password=dbconfig['password'])
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {dbconfig['database']}")
        conn = mysql.connector.connect(**dbconfig)


cursor = conn.cursor()

# def login(username: str, password: str):
	
class database():
    def __init__():
        username = None

    def register(self):
        pass

    def checktable(self, tablename):
        cursor.execute(f"SHOW TABLES LIKE {tablename}")

    def curDatebase(self):
        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchall()
        return result[0][0]



    def login(self, username: str, passcode: str):
        cursor.excute(f"")



if False:
    cursor.execute("SELECT DATABASE()")



