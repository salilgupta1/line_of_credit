# Wrapper class for Acccounts table
from models.datastore.PostgresSQL import PostgresSQL

class AccountManager:

	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def createAccount(self, vals):

		# create a new account associated with a user
		query = """INSERT INTO "accounts" (user_name, credit_limit, apr, principal, date_created) VALUES (%s,%s,%s,%s,%s) returning account_id;"""

		return self.PostgresSQL.insert(query, vals)

	def verifyUser(self, account_id):
		query ="""SELECT user_name FROM "accounts" where account_id=%s""";
		return self.PostgresSQL.read(query, (account_id,))

	def updatePrincipal(self, new_principal, accountid):

		# update the principal balance
		query = """UPDATE "accounts" set principal = principal + %s where account_id=%s;"""

		vals = (new_principal,accountid)
		
		return self.PostgresSQL.update(query,vals)

	def getAccountData(self, account_id):

		# get meta data for a single account
		query = """SELECT principal, credit_limit, apr, date_created FROM "accounts" where account_id=%s;"""
		vals = (account_id,)

		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result, ("principal","credit_limit","apr","date_created"))

	def getAccounts(self, username):
		
		# get all accounts associated with a user
		query = """SELECT account_id FROM "accounts" where user_name=%s;"""
		vals = (username,)

		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result, ("id",))