####
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
