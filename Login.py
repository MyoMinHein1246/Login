from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys


FILE_NAME = "database.txt"


class MsgBox():
	def show(self, icon, title: str, msg:str):
		msgBox = QMessageBox(icon,title, msg)
		msgBox.setInformativeText("Please try again.")
		msgBox.exec()
		print(msg)


class LoginCheck():
	def __init__(self, parent) -> None:
		self.editUsername = parent.editUsername
		self.editPassword = parent.editPassword

	def tryLogin(self) -> str:
		username = self.editUsername.text()
		password = self.editPassword.text()

		dataDict = self.getDataDict()
		return self.login(username, password, dataDict)

	def login(self, username: str, password: str, dataDict: list) -> str:
		msg = "Could not fine any user with the username."
		
		if not dataDict:
			msg = "Could not fine any user with the username."
			return msg
		for data in dataDict:
			if data['username'] == username:
				if data['password'] == password:
					msg = "Login success!"
					break
				else:
					msg = "Wrong password!"
					break

		return msg

	def createNewAccount(self) -> str:
		username = self.editUsername.text()
		password = self.editPassword.text()

		msg = ""

		if self.checkUsername(username):
			msg = "User already existed with the username."
			return

		with open(FILE_NAME, 'a') as f:
			try:
				f.write("\n{}, {}".format(username, password))
				msg = "User created successfully!"
			except Exception:
				msg = "Error while writing data."
				return
			
		return msg

	def getDataDict(self) -> list:
		dataDict = list(dict())

		with open(FILE_NAME, 'r') as f:
			for line in f.readlines():
				username = line.split(',')[0].strip()
				password = line.split(',')[1].strip()
				data = {'username':username, 'password':password}
				dataDict.append(data)

		return dataDict

	def checkUsername(self, username: str, dataDict:list = list()) -> bool:
		if len(dataDict) == 0:
			dataDict = self.getDataDict()

		for data in dataDict:
			if data['username'] == username.strip():
				return True

		return False


class LoginForm(QDialog):
	def __init__(self) -> None:
		super(LoginForm, self).__init__()
		uic.loadUi("LoginForm.ui", self)
		
		self.msgBox = MsgBox()

		loginCheck = LoginCheck(self)

		self.btnLogin.clicked.connect(lambda: self.msgBox.show(QMessageBox.Information, "Login", loginCheck.tryLogin()))
		self.btnCreate.clicked.connect(lambda: self.msgBox.show(QMessageBox.Information, "Create", loginCheck.createNewAccount()))
		self.btnClose.clicked.connect(self.exit)
		
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

