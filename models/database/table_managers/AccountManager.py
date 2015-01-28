# Wrapper class for Acccounts table
from models.datastore.PostgresSQL import PostgresSQL

class AccountManager:

	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def createAccount(self, vals):

		# create a new account associated with a user
		query = """INSERT INTO "accounts" (user_name, credit_limit, apr) VALUES (%s,%s,%s) returning account_id;"""

		return self.PostgresSQL.insert(query, vals,fetch=True)

	def verifyUser(self, account_id):
		query ="""SELECT user_name FROM "accounts" where account_id=%s""";
		return self.PostgresSQL.read(query, (account_id,))

	def updateCredit(self, delta_principal, account_id):

		# update the principal balance
		query = """UPDATE "accounts" set principal = principal + %s, credit_limit = credit_limit - %s WHERE account_id=%s returning principal, apr;"""

		vals = (delta_principal, delta_principal, account_id)
		
		return self.PostgresSQL.update(query,vals,fetch=True)

	def updateInterest(self, interest, account_id):
		query = """UPDATE "accounts" set interest =  %s WHERE account_id=%s;"""
		vals = (interest, account_id)
		self.PostgresSQL.update(query,vals)

	def getAccountData(self, account_id):

		# get meta data for a single account
		query = """SELECT principal, credit_limit, apr, interest FROM "accounts" where account_id=%s;"""
		vals = (account_id,)

		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result, ("principal","credit_limit","apr","interest"))

	def getAccounts(self, username):
		
		# get all accounts associated with a user
		query = """SELECT account_id FROM "accounts" where user_name=%s;"""
		vals = (username,)

		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result, ("id",))