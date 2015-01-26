from models.database.table_managers.AccountManager import AccountManager
from models.database.table_managers.TransactionManager import TransactionManager
import datetime
class AccountController():

	def __init__(self):
		self.AccountManager = AccountManager()
		self.TransactionManager = TransactionManager()

	def createAccount(self, username, credit_limit, apr):
		date_created = datetime.date.today().strftime("%Y-%m-%d")
		vals = (username, credit_limit, apr, 0.0, date_created)
		return self.AccountManager.createAccount(vals)[0][0]

	def getAccounts(self, username):
		return self.AccountManager.getAccounts(username)['results']

	def getAccountData(self, username, account_id):
		user = self.AccountManager.verifyUser(account_id)
		if user[0][0] == username:
			results = self.AccountManager.getAccountData(account_id)
			return results['results']
		else:
			# we know the account id is not associated with the user
			# ideally raise a custom exception
			return False

	def createTransaction(self, account_id, amount, trans_type):
		date_created = datetime.date.today().strftime("%Y-%m-%d")
		self.TransactionManager.createTransaction((account_id, date_created, amount, trans_type))
		principal = 0
		if trans_type == "draw":
			principal = amount
		else:
			principal = str(int(amount)*-1)

		self.AccountManager.updatePrincipal(principal, account_id)

		# function to update interest here ...
		
	def viewTransactions(self, username, account_id):
		user = self.AccountManager.verifyUser(account_id)
		if user[0][0] == username:
			results =  self.TransactionManager.getTransactions(account_id)
			return results['results']
		else:
			# we know the account id is not associated with the user
			# ideally raise a custom exception
			return False
