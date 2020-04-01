#!/bin/sh
daphne jderobot_server.asgi:channel_layer --port 8000 -v 2
#nano aaaa
ret=$?
log=daphne_killed.log
echo $ret > $log
if [ $ret -eq 0 ]; then
  echo "The program exited normally" >> $log 
elif [ $ret -gt 128 ]; then
  echo "The program died of signal $((ret-128)): $(kill -l $ret)" >> $log
  dmesg > dmseg.log
else
  echo "The program failed with status $ret" >> $log
fi
