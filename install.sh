#!/usr/bin/env sh

HERE=$(dirname $0)
[ -h $0 ] && HERE=$(dirname $(readlink $0))

THERE=$HOME/.mcabber

cp $HERE/start.sh $THERE/start.sh
cp $HERE/stop.sh $THERE/stop.sh
cp $HERE/eventcmd $THERE/eventcmd
cp $HERE/mcabbernotify.py $THERE/mcabbernotify.py
cp $HERE/mcabber_wrapper $THERE/mcabber_wrapper
touch $THERE/last_event
