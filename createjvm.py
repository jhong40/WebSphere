mynode='Node1'
myjvm='Server1'
jvmmin='512'
jvmmax='1025'

try:
  AdminTask.deleteServer('[-serverName '+ myjvm + ' -nodeName '+ mynode + ']')
except:
  print("testabc doesn't exist, will create one....")

AdminTask.createApplicationServer(mynode, '[-name ' + myjvm + ' -templateName default -genUniquePorts true ]')
AdminTask.setJVMInitialHeapSize('[-serverName ' + myjvm + ' -nodeName ' + mynode + ' -initialHeapSize 1111]')
AdminTask.setJVMMaxHeapSize('[-serverName ' + myjvm + ' -nodeName ' + mynode + ' -maximumHeapSize 4445]')
AdminTask.setJVMSystemProperties('[-serverName ' + myjvm + ' -nodeName ' + mynode + ' -propertyName  test.property -propertyValue testValue]')
AdminTask.setJVMSystemProperties('[-serverName ' + myjvm + ' -nodeName ' + mynode + ' -propertyName  aaa  -propertyValue bbb]')


#appSrv=AdminConfig.getid('/Node:' + mynode + '/Server:' + myjvm + '/ApplicationServer:/')
#AdminConfig.modify(appSrv, '[[applicationClassLoaderPolicy "SINGLE"] [applicationClassLoadingMode "PARENT_LAST"]]')


### Web container custom prop
propertyName = 'aaa'
propertyValue = 'bbb'

server = AdminConfig.getid('/Server:testabc')
wc = AdminConfig.list('WebContainer',server)
attr = [['name',propertyName],['value',propertyValue]]
AdminConfig.create('Property', wc, attr)
AdminConfig.save()


### Session timeout
server=AdminConfig.getid('/Node:node1/Server:server1')
#AdminConfig.modify(server, '[ [invalidationTimeout "10"] ]')
#AdminConfig.modify(server, '[[allowOverflow "true"] [invalidationTimeout "80"] [maxInMemorySessionCount "1000"]]')

sms=AdminConfig.list("SessionManager",server)
AdminConfig.modify(sms,'[[tuningParams [[allowOverflow "true"] [invalidationTimeout "10"] [maxInMemorySessionCount "1000"]]]]')



AdminConfig.save()
