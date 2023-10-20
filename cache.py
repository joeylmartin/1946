class Cache():
	def __init__(self, load_command):
		self.cache = {}
		self.load_command = load_command
	
	def fetch(self, key_tuple):
		try:
			return self.cache[key_tuple]
		except:
			self.cache[key_tuple] = self.load_command(*key_tuple)
			return self.cache[key_tuple]