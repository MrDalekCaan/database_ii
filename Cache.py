from time import time


class Cache(dict):
	def __init__(self, life_time, delete=None):
		"""
		Call delete(key, value) when an item will be delete from Cache.
		Cache won't refresh until __getitem__ is called.
		:param life_time:
		:param delete:
		"""
		super(Cache, self).__init__()
		self.life_time = life_time
		self.parent = super(Cache, self)
		self.delete = delete if delete is not None else lambda x, y: x

	def refresh(self):
		now = time()
		for k in list(self.parent.keys()):
			if now - self.parent.__getitem__(k)[1] > self.life_time:
				self.delete(k, self.parent.__getitem__(k)[0])
				self.parent.__delitem__(k)
		return now

	def __getitem__(self, key):
		now = self.refresh()
		self.parent.__getitem__(key)[1] = now
		return self.parent.__getitem__(key)[0]

	def __setitem__(self, key, value):
		now = time()
		super(Cache, self).__setitem__(key, [value, now])