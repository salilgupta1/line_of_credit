# Wrapper class for Users table
from models.datastore.PostgresSQL import PostgresSQL

class UserManager:

	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def createUser(self,vals):
		# insert a user into the db
		
		query = """INSERT INTO "users" VALUES (%s,%s,%s,%s);"""
		self.PostgresSQL.insert(query,vals)
		
	def getUserAuth(self, username):
		# get user auth for login
		
		query = """SELECT password, password_salt from "users" where username=%s;"""
		vals = (username,)

		return self.PostgresSQL.read(query,vals)
