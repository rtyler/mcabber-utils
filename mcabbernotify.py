#!/usr/bin/env python

import os
import sys
import time

LOW = -1
NORMAL = -2
CRITICAL = -3

def notifier_init():
	if sys.platform == 'linux2':
		import pynotify
		pynotify.init('mcabber')
def notifier_close():
	if sys.platform == 'linux2':
		import pynotify
		pynotify.uninit()

def generateNotification(title, body, urgency=LOW):
	if sys.platform == 'linux2':
		import pynotify
		urg = {LOW : pynotify.URGENCY_LOW, NORMAL : pynotify.URGENCY_NORMAL, CRITICAL : pynotify.URGENCY_CRITICAL}
		n = pynotify.Notification(title, body)
		n.set_timeout(4500)
		n.set_urgency(urg[urgency])
		n.show()
	if sys.platform == 'darwin':
		os.system('growlnotify --name="mcabber" %s' % ('%s\n%s' % (title, body)))

class Handlers(object):
	def STATUS(self, line):
		status_map = {'O' : 'online', '_' : 'offline', 'A' : 'away', 'I' : 'invisible', 'F' : 'free to chat', 'D' : 'do not disturb', 'N' : 'not available'}
		parts = line.split(' ')
		cmd = parts[0]
		status = parts[1]
		who = ' '.join(parts[2:])
		who = ''.join([f for f in who if f != '\n'])
		status = status_map.get(status, status)
		generateNotification('%s is now %s' % (who, status), '')

	def UNREAD(self, line):
		parts = line.split(' ')
		unread = int(parts[1])
		if unread > 1:
			generateNotification('%s unread messages' % unread, '')

	def MSG(self, line):
		parts = line.split(' ')
		cmd = parts[0]
		kind = parts[1]
		who = ' '.join(parts[2:])
		who = ''.join([f for f in who if f != '\n'])
		if kind == 'IN':
			generateNotification('Private message', '%s sent you a message' % who, CRITICAL)
		if kind == 'MUC':
			generateNotification('Conference activity in', who, NORMAL)
		

def main():
	h = Handlers()
	notifier_init()
	while True:
		line = sys.stdin.readline()
		if line:
			cmd = line.split(' ')[0]
			if hasattr(h, cmd):
				getattr(h, cmd)(line) 
			else:
				print line
		time.sleep(1)
	notifier_close()

if __name__ == '__main__':
	main()

