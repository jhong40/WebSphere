# WebSphere

```
# find all the file under . and replace aaa with bbb
find . -type f -print0  | xargs -0 sed -i 's/host1/host2/g'  
```

# AIX
#### Account reset and unlock
```
lsuser <userid>  # check user info: locked status, unsuccessful_login_count, etc
lsuser -a unsuccessful_login_count <userid>   # list unsuccessful_login_count
chsec -f /etc/security/lastlog -a unsuccessful_login_count=0 -s <userid>     # reset unsuccessful_login_count
chuser account_locked=false <userid>  # unlock 
chuser account_locked=true <userid>  # lock 
```

#### Find which process using port
https://support.spirent.com/SC_KnowledgeView?Id=FAQ14250<br>
https://www.ibm.com/support/pages/finding-which-program-using-port-aix

```
#ps -aef |grep 8080
    root 6357050 7405584   0 11:34:02  pts/0  0:00 grep 8080
#netstat -Aan |grep 8080
f1000500038203b8 tcp        0      0  *.8080                *.*                   LISTEN
# rmsock f1000500038203b8 tcpcb
The socket 0xf100050003820008 is being held by proccess 4325554 (javaw).
```

# WebSphere MQ
#### RUNMQSC
```
cd /usr/mqm/bin
./runmqsc NJKAOCDE

DISPLAY Q(MYQ)
```

#### Browse Message in Q
```
cd /usr/mqm/samp/bin
./amqsbcg Q Qmgr 
```
#### Setup MQ Web UI
https://developer.ibm.com/tutorials/mq-setting-up-using-ibm-mq-console/#step-1-set-up-the-mq-console
https://www.ibm.com/docs/en/ibm-mq/9.3?topic=api-basic-configuration-mqweb-server
```
cp /usr/mqm/web/mq/samp/configuration/basic_registry.xml    /var/mqm/web/installations/Installation1/servers/mqweb
#  0. cp basic_registry.xml mqwebuser.xml  (mk a copy mqwebuser.xml before hand)
#  1. change mqadmin pass
#  2. <variable name="httpsPort" value="9443"/>
#  3. <virtualHost allowFromEndpointRef="defaultHttpEndpoint" id="default_host">
#        <hostAlias>localhost:9444</hostAlias>
#        <hostAlias>localhost:8002</hostAlias>
#    </virtualHost>
export WLP_USR_DIR=/var/mqm/web/installations/Installation1
setmqweb properties -k httpHost -v "*"
strmqweb
endmqweb
```
