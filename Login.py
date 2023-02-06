from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys


FILE_NAME = "database.txt"


class LoginForm(QDialog):
	def __init__(self) -> None:
		super(LoginForm, self).__init__()
		uic.loadUi("LoginForm.ui", self)
		self.btnLogin.clicked.connect(self.tryLogin)
		self.btnCreate.clicked.connect(self.createNewAccount)
		self.btnClose.clicked.connect(self.exit)

	def tryLogin(self):
		username = self.editUsername.text()
		password = self.editPassword.text()

		dataDict = self.getDataDict()
		print(self.login(username, password, dataDict))

	def login(self, username: str, password: str, dataDict: list) -> str:
		msg = "Could not fine any user with the username."
		
		if not dataDict:
			msg = "Could not fine any user with the username."
			return msg
		for data in dataDict:
			if data['username'] == username.strip():
				if data['password'] == password.strip():
					msg = "Login success!"
					break
				else:
					msg = "Wrong password!"
					break

		return msg

	def createNewAccount(self):
		username = self.editUsername.text()
		password = self.editPassword.text()

		with open(FILE_NAME, 'a') as f:
			try:
				f.write("\n{}, {}".format(username, password))
			except Exception:
				print("Error while writing data.")
				return
			
			print("User created successfully!")

	def getDataDict(self) -> list:
		dataDict = list(dict())

		with open(FILE_NAME, 'r') as f:
			for line in f.readlines():
				username = line.split(',')[0].strip()
				password = line.split(',')[1].strip()
				data = {'username':username, 'password':password}
				dataDict.append(data)

		return dataDict

	def exit(self):
		self.close()


def main():
	app = QApplication.instance()
	if not app:
		app = QApplication([])

	form = LoginForm()
	form.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

