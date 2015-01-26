# Wrapper class for Transactions table
from models.datastore.PostgresSQL import PostgresSQL

class TransactionManager:

	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def createTransaction(self, vals):
		# create a transaction for a certain account
		query = """INSERT INTO "transactions" (accountid, date_of_transaction, amount, trans_type) VALUES (%s,%s,%s,%s);"""

		self.PostgresSQL.insert(query, vals)

	def getTransactions(self, account_id):
		# return all transactions associated with an account

		query = """SELECT date_of_transaction, amount, trans_type FROM "transactions" where accountid=%s;"""
		vals = (account_id,)

		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result,("date_of_transaction","amount","trans_type"))