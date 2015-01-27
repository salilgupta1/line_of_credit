from models.database.table_managers.UserManager import UserManager
import os, hashlib, datetime

class UserController():

	def __init__(self):
		self.UserManager = UserManager()

	def authenticateUser(self,username, password):
		try:
			result = self.UserManager.getUserAuth(username)
			if len(result) > 0:
				db_password = result[0][0]
				db_salt = result[0][1]
				password = password + db_salt
				hashed = hashlib.sha1(password).hexdigest()
				if (hashed == db_password):
					return True
			return "Oops! Invalid Username or Password...."
		except:
			raise

	def registerUser(self, username, password):
		try:
			# create salt and encrypt password
			salt = os.urandom(16).encode('base-64')
			password+=salt
			password = hashlib.sha1(password).hexdigest()

			vals = (username, password, salt)
			self.UserManager.createUser(vals)
			return True
		except:
			return "Username is already taken!"
			raise

