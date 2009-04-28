#!/usr/bin/env sh

DIR=$HOME/.mcabber

[ -f $DIR/notify_pids ] && cat $DIR/notify_pids | xargs kill && rm $DIR/notify_pids
