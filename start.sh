#!/usr/bin/env sh

DIR=$HOME/.mcabber

pidtail() {
	tail -F $1 &
	echo $! 1>&2
}

echo -n > $DIR/notify_pids
echo -n > $DIR/last_event
(pidtail $DIR/last_event 2>> $DIR/notify_pids | python $DIR/mcabbernotify.py 2>> $DIR/notify_pids) &
echo $! >> $DIR/notify_pids
