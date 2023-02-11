from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import sqlite3


def resource_path(relative_path) -> str:
    import os, sys

    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class MsgBox():
	def show(self, icon, title: str, msg:str):
		msgBox = QMessageBox(icon,title, msg)
		msgBox.exec()
		print(msg)


class LoginCheck():
	def __init__(self, parent, cursor) -> None:
		self.editUsername = parent.editUsername
		self.editPassword = parent.editPassword
		self.cursor = cursor

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
			return msg

		try:
			self.cursor.execute("INSERT INTO login(username, password) VALUES(?, ?);", (username, password))
			msg = "User created successfully!"
		except Exception:
			msg = "Error while writing data."
		finally:
			return msg

	def getDataDict(self) -> list:
		dataDict = list(dict())

		self.cursor.execute("SELECT * FROM login;")
		
		for data in self.cursor.fetchall():
			id = data[0]
			username = data[1].strip()
			password = data[2].strip()
			data = { 'id': id, 'username':username, 'password':password }
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
	def __init__(self, cursor) -> None:
		super(LoginForm, self).__init__()
		uic.loadUi(resource_path("./Resources/LoginForm.ui"), self)
		
		self.msgBox = MsgBox()

		loginCheck = LoginCheck(self, cursor)

		self.btnLogin.clicked.connect(lambda: self.msgBox.show(QMessageBox.Information, "Login", loginCheck.tryLogin()))
		self.btnCreate.clicked.connect(lambda: self.msgBox.show(QMessageBox.Information, "Create", loginCheck.createNewAccount()))
		self.btnClose.clicked.connect(self.exit)
		
	def exit(self):
		self.close()


def main():
	try:
		app = QApplication.instance()
		if not app:
			app = QApplication([])
		
		connection = sqlite3.connect(resource_path("./Resources/LoginData.db"))
		cursor = connection.cursor()

		form = LoginForm(cursor)
		form.show()

		code = app.exec_()

	except sqlite3.Error as err:
		print(err)

	finally:
		if cursor:
			connection.commit()
			cursor.close()
			connection.close()

		sys.exit(code)


if __name__ == "__main__":
	main()

