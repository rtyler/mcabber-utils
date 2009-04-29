#!/usr/bin/env python

import locale
import os
import re
import sys
import time

LOW = -1
NORMAL = -2
CRITICAL = -3
MAX_MSG_LEN = 60
PAUSE = 0.2
encoding = locale.getdefaultlocale()[1]

def notifier_init():
	if sys.platform == 'linux2':
		import pynotify
		pynotify.init('mcabber')

def notifier_close():
	if sys.platform == 'linux2':
		import pynotify
		pynotify.uninit()

if sys.platform == 'linux2':
	def generateNotification(title, body, urgency=LOW):
		import pynotify
		urg = {LOW : pynotify.URGENCY_LOW, NORMAL : pynotify.URGENCY_NORMAL, CRITICAL : pynotify.URGENCY_CRITICAL}
		n = pynotify.Notification(unicode(title, encoding), unicode(body, encoding))
		n.set_timeout(4500)
		n.set_urgency(urg[urgency])
		n.show()
elif sys.platform == 'darwin':
	def generateNotification(title, body, urgency=LOW):
		os.system('growlnotify --name="mcabber" -m "%s"' % ('%s\n%s' % (title, body)))

class Handlers(object):
	status_map = {'O' : 'online', '_' : 'offline', 'A' : 'away', 'I' : 'invisible', 'F' : 'free to chat', 'D' : 'do not disturb', 'N' : 'not available'}

	arg_re = re.compile("\(.*?\)")
	def parse(self, line):
		parts = [x[1:-1] for x in self.arg_re.findall(line)]
		cmd = parts[0]
		kind = parts[1]
		who = len(parts) > 2 and parts[2] or None
		return parts, cmd, kind, who

	def STATUS(self, line):
		parts, cmd, kind, who = self.parse(line)
		generateNotification('%s is now %s' % (who, self.status_map.get(kind)), '')

	def UNREAD(self, line):
		parts, cmd, kind, who = self.parse(line)
		unread = int(parts[1])
		if unread > 1:
			generateNotification('%s unread messages' % unread, '')

	def MSG(self, line):
		parts, cmd, kind, who = self.parse(line)
		if len(parts) > 3:
			fname = parts[3].rstrip()
			fp = open(fname)
			msg = fp.read().rstrip()
			fp.close()
			os.remove(fname)
			if len(msg) > MAX_MSG_LEN:
				msg = msg[:MAX_MSG_LEN] + '...'
		else:
			msg = ''

		if kind == 'IN':
			generateNotification('%s sent you a message' % who, msg, CRITICAL)
		if kind == 'MUC':
			generateNotification('Conference activity in', who, NORMAL)


def main():
	print >> sys.stderr, "%d\n" % os.getpid()
	h = Handlers()
	notifier_init()
	try:
		while True:
			line = sys.stdin.readline()
			if line:
				cmd = Handlers.arg_re.findall(line)[0][1:-1]
				if hasattr(h, cmd):
					getattr(h, cmd)(line)
				else:
					print line
            time.sleep(PAUSE)
	finally:
		notifier_close()

if __name__ == '__main__':
	main()

