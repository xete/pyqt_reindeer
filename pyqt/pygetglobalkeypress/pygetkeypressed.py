#!/usr/bin/python

WARNINGS='''
# make sure you have correctly set up environment 
# eventually with pygs module
# Thanks to providing pygs: https://github.com/Asvel/pygs
# APIs: http://libqxt.bitbucket.org/doc//tip/qxtglobalshortcut.html
# Test passed Ubuntu 14.04 LTS, pyqt4.
'''

ERR_CODE = {"ImportError": 1}

import sys
try:
	from PyQt4.QtGui import QApplication, QSystemTrayIcon, QKeySequence
	from pygs import QxtGlobalShortcut
except:
	print WARNINGS
	sys.exit(ERR_CODE["ImportError"])





class contentholder():
	def __init__(self):
		self.content = None
		pass
	
	def contentchanged(self):
		content = app.clipboard().text()
		print content

	def handlecontent(self, content):
		pass


SHORTCUT_COPY='Ctrl+C'

class application(QApplication):
	def __init__(self, argv):
		QApplication.__init__(self,argv)
		self.shortcut_copy = QxtGlobalShortcut()
		self.shortcut_copy.setShortcut(QKeySequence(SHORTCUT_COPY))
		self.holder = contentholder()
		self.shortcut_copy.activated.connect(self.holder.contentchanged)


if __name__ == '__main__':
	app = application(sys.argv)
	sys.exit(app.exec_())

