import threading


class MysqlCursorWrapper:
	def __init__(self, cursor):
		self._cursor = cursor
		self._lock = threading.Lock()
		self.fetchall = self._cursor.fetchall
		self.fetchone = self._cursor.fetchone

	def execute(self, statement):
		self._lock.acquire()
		self._cursor.execute(statement)
		self._lock.release()



