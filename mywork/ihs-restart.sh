pid=`ps -ef | grep httpd | grep -v grep | awk '{print $2}'`
echo Initial IHS Process: $pid

/u01/app/HTTPServer/bin/apachectl -f conf/httpd_njkids.conf -k stop
/u01/app/HTTPServer/bin/apachectl -f conf/httpd_ocse.conf -k stop
/u01/app/HTTPServer/bin/apachectl -f conf/httpd_cusw.conf -k stop

pid=`ps -ef | grep httpd | grep -v grep | awk '{print $2}'`
echo After Stop, Still alive: $pid

i=0
while [[ "x$pid" != "x" ]] && [[ i -le 10 ]]   #wait for 10 sec for the httpd instance to end
do
  echo $i $pid
  pid=`ps -ef | grep httpd | grep -v grep | awk '{print $2}'`
  sleep 1
  i=$((i+1))
done

echo "done with while loop"

if  [[ "x$pid" != "x" ]] ; then
  echo "kill pid running"
  kill -9 $pid
fi

sleep 1
pid=`ps -ef | grep httpd | grep -v grep | awk '{print $2}'`
echo Final PID check: $pid \(should be nothing\)

/u01/app/HTTPServer/bin/apachectl -f conf/httpd_njkids.conf -k start
/u01/app/HTTPServer/bin/apachectl -f conf/httpd_ocse.conf -k start
/u01/app/HTTPServer/bin/apachectl -f conf/httpd_cusw.conf -k start

ps -ef | grep httpd | grep -v grep
