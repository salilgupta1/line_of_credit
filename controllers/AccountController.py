from models.database.table_managers.AccountManager import AccountManager
from models.database.table_managers.TransactionManager import TransactionManager

class AccountController():

	def __init__(self):
		self.AccountManager = AccountManager()
		self.TransactionManager = TransactionManager()

	def createAccount(self, username, credit_limit, apr):
		vals = (username, credit_limit, apr, 0.0)
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

	def createTransaction(self, account_id, transaction_day, amount, trans_type):
		delta_principal = 0
		if trans_type == "draw":
			delta_principal = amount
		else:
			delta_principal = str(int(amount)*-1)

		(new_principal, apr) = self.AccountManager.updateCredit(delta_principal, account_id)[0]
		
		self.TransactionManager.createTransaction((account_id, transaction_day, amount, trans_type, new_principal))

		interest = self.__calculateInterest(account_id, apr)

		self.AccountManager.updateInterest(interest,account_id)

	def __calculateInterest(self, account_id, apr):
		result = self.TransactionManager.getInterestData(account_id)
		interest = 0.0
		i = 0
		while i < len(result):
			days = 0
			if i == len(result)-1:
				days = 30 - result[i][0]
			else:
				days = result[i+1][0] - result[i][0]
			interest += float(result[i][1] * days/365 * apr)
			i += 1
		return interest

	def getTransactions(self, username, account_id):
		user = self.AccountManager.verifyUser(account_id)
		if user[0][0] == username:
			results =  self.TransactionManager.getTransactions(account_id)
			return results['results']
		else:
			# we know the account id is not associated with the user
			# ideally raise a custom exception
			return False
