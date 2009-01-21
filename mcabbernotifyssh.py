#!/usr/bin/env python

import os
import sys
import time

LOW = -1
NORMAL = -2
CRITICAL = -3

def runssh():
	print '==> Logging in'
	os.system('ssh pineapple -C "tail -f ~/.mcabber/last_event" > /tmp/mcabber 2>&1 &')

def notifier_init():
	if sys.platform == 'linux':
		import pynotify
		pynotify.init('mcabber')
def notifier_close():
	if sys.platform == 'linux':
		import pynotify
		pynotify.uninit()

def generateNotification(title, body, urgency=LOW):
	if sys.platform == 'linux':
		import pynotify
		urg = {LOW : pynotify.URGENCY_LOW, NORMAL : pynotify.URGENCY_NORMAL, CRITICAL : pynotify.URGENCY_CRITICAL}
		n = pynotify.Notification(title, body)
		n.set_timeout(4500)
		n.set_urgency(urg[urgency])
		n.show()
	if sys.platform == 'darwin':
		pass # import GrowlNotify?

class Handlers(object):
	def STATUS(self, line):
		status_map = {'O' : 'online', '_' : 'offline', 'A' : 'away', 'I' : 'invisible', 'F' : 'free to chat', 'D' : 'do not disturb', 'N' : 'not available'}
		parts = line.split(' ')
		cmd = parts[0]
		status = parts[1]
		who = ' '.join(parts[2:])
		status = status_map.get(status, status)
		generateNotification('Status Change', '%s is now %s' % (who, status))

	def UNREAD(self, line):
		parts = line.split(' ')
		unread = int(parts[1])
		if unread > 1:
			generateNotification('You have unread Jabber messages', '%s total unread messages' % unread)

	def MSG(self, line):
		parts = line.split(' ')
		cmd = parts[0]
		kind = parts[1]
		who = ' '.join(parts[2:])
		if kind == 'IN':
			generateNotification('Private message:', '%s sent you a message' % who, CRITICAL)
		if kind == 'MUC':
			generateNotification('Conference activity in:', who, NORMAL)
		

def main():
	runssh()
	f = open('/tmp/mcabber', 'r')
	h = Handlers()
	notifier_init()
	while True:
		line = f.readline()
		if line:
			cmd = line.split(' ')[0]
			if hasattr(h, cmd):
				getattr(h, cmd)(line) 
			else:
				print line
		time.sleep(1)
	f.close()
	notifier_close()

if __name__ == '__main__':
	main()
