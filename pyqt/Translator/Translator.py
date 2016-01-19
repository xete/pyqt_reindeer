#!/usr/bin/python

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from Codec.trans import dec

class clickableTextEdit(QTextEdit):
	def __init__(self, readonly = False, parent = None):
		QTextEdit.__init__(self, parent)
		self.setReadOnly(readonly)
		self.doubleClicked_callback = None

	# re-implement mouseDoubleClickEvent
	def mouseDoubleClickEvent(self, e): 
		if self.doubleClicked_callback:
			self.doubleClicked_callback(self, e)


class viewlayout(QVBoxLayout):
	def __init__(self, parent = None):
		QVBoxLayout.__init__(self, parent)
	

	def prepare(self):

		# the first row
		fir_row = QHBoxLayout()
		text = clickableTextEdit()
		def input_double_callback(obj, e):
			# QClipboard.text() not toPlainText()
			obj.setText(app.clipboard().text())
		text.doubleClicked_callback = input_double_callback
		text.setGeometry(50, 50, 10, 100)
		text.setReadOnly(False) # True in python, not true
		fir_row.addWidget(text)

		btnlyt = QVBoxLayout()

		trans = QPushButton('translate')
		def translate():
			result.setText(dec(text.toPlainText()))
		trans.clicked.connect(lambda: translate())
		btnlyt.addWidget(trans)

		def clt():
			text.clear()
			result.clear()
		clean = QPushButton('clean')
		clean.clicked.connect(lambda: clt())
		btnlyt.addWidget(clean)

		quit = QPushButton('quit')
		btnlyt.addWidget(quit)
		self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
		fir_row.addLayout(btnlyt)
		self.addLayout(fir_row)


		# the second row
		sec_row = QHBoxLayout()
		result = clickableTextEdit(True) 
		def output_double_callback(obj, e):
			app.clipboard().setText(obj.toPlainText())
		result.doubleClicked_callback = output_double_callback
		result.setReadOnly(True)
		result.setText('double click to paste input\nEnter to translate\ndouble click to clipboard')
		sec_row.addWidget(result)
		self.addLayout(sec_row)


class mainentry(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.setWindowTitle('Translator')
		self.setGeometry(100, 100, 600, 400)
		layout = viewlayout(self)
		layout.prepare()

class SystemTrayIcon(QtGui.QSystemTrayIcon):
	def __init__(self, icon, parent = None):
		QtGui.QSystemTrayIcon.__init__(self, icon, parent) 
		menu = QtGui.QMenu(parent)
		hideAction = menu.addAction(QtGui.QAction('&Hide', self, triggered = self.hide)) 
		exitAction = QtGui.QAction('&Quit', self, triggered = app.quit)
		menu.addAction(exitAction)
		self.setContextMenu(menu)
	
	def hide(self):
		if w.isHidden():
			w.show()
		else:
			w.hide()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	w = mainentry() 
	if QtGui.QSystemTrayIcon.isSystemTrayAvailable():
		# trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("Translator.xpm"), w)
		trayIcon = SystemTrayIcon(QtGui.QIcon("Translator.xpm"), w)
		trayIcon.show()
	w.show()
	sys.exit(app.exec_())

