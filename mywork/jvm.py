mynode='node01'
myjvm='testabc'
jvmmin='512'
jvmmax='1025'

jvmargdict={
  "aaa":"aaa1",
  "bbb":"bbb1"
}
webcontainer_argdict={
  "aaa":"aaa1",
  "bbb":"bbb1"
}

cellName = AdminControl.getCell()

try:
  AdminTask.deleteServer('[-serverName '+ myjvm + ' -nodeName '+ mynode + ']')
  print("Deleting JVM: "+ myjvm)
except:
  print(myjvm + " doesn't exist, will create one....")
AdminConfig.save()


### Create JVM and set JVM init/max size
serv=AdminTask.createApplicationServer(mynode, '[-name ' + myjvm + ' -templateName default -genUniquePorts true ]')
AdminTask.setJVMInitialHeapSize('[-serverName ' + myjvm + ' -nodeName ' + mynode + ' -initialHeapSize '+ jvmmin +']')
AdminTask.setJVMMaxHeapSize('[-serverName ' + myjvm + ' -nodeName ' + mynode + ' -maximumHeapSize '+ jvmmax +']')

### JVM custom prop
for myn, myv in jvmargdict.items():
  #print (myn, myv)
  AdminTask.setJVMSystemProperties('[-serverName ' + myjvm + ' -nodeName ' + mynode + ' -propertyName '+ myn + ' -propertyValue '+ myv +']')


### Classloader policy 
#appSrv=AdminConfig.getid('/Node:' + mynode + '/Server:' + myjvm + '/ApplicationServer:/')
#AdminConfig.modify(appSrv, '[[applicationClassLoaderPolicy "SINGLE"] [applicationClassLoadingMode "PARENT_LAST"]]')


### Web container custom prop 
wc = AdminConfig.list('WebContainer',serv)
for myn, myv in webcontainer_argdict.items():
  attr = [['name',myn],['value',myv]]
  AdminConfig.create('Property', wc, attr)


### Session timeout 
sms=AdminConfig.list("SessionManager",serv)
AdminConfig.modify(sms,'[[tuningParams [[allowOverflow "true"] [invalidationTimeout "10"] [maxInMemorySessionCount "1000"]]]]')

### Cookie Restrict to HTTPS Session
#AdminServerManagement.configureCookieForServer(mynode, myjvm, "JSESSIONID", "", -1, "true", [["path", "/"]])
webcont=AdminConfig.list('WebContainer',serv)
sessman=AdminConfig.list('SessionManager',webcont)
cookies=AdminConfig.showAttribute(sessman,'defaultCookieSettings')
AdminConfig.showall(cookies)
#attrs=['name', 'CookieName']
attrs=['secure', 'true']
AdminConfig.modify(cookies,[attrs])
AdminConfig.showall(cookies)


### Web Container Thread Pool: 10,50,3500
threadPools=AdminConfig.list('ThreadPool',serv)
threadPoolList=AdminUtilities.convertToList(threadPools)
for tps in threadPoolList:
  if AdminConfig.showAttribute(tps,'name') == 'WebContainer':
    webcontainerThreadPoolID=tps
AdminConfig.modify(webcontainerThreadPoolID, '[[maximumSize "50"] [name "WebContainer"] [minimumSize "10"] [inactivityTimeout "3500"] [description ""] [isGrowable "false"]]')

### JVM Logs SystemOut.log SystemErr.log maxsize:10, starttime:24, repeat time:12 max hist file:14
log = AdminConfig.showAttribute(serv, 'outputStreamRedirect')
AdminConfig.modify(log, [['rolloverType', 'TIME'], ['rolloverPeriod', 12], ['baseHour', 24], ['rolloverSize',10], ['maxNumberOfBackupFiles',14], ['rolloverType','BOTH'] ])

log = AdminConfig.showAttribute(serv, 'errorStreamRedirect')
AdminConfig.modify(log, [['rolloverType', 'TIME'], ['rolloverPeriod', 12], ['baseHour', 24], ['rolloverSize',10], ['maxNumberOfBackupFiles',14], ['rolloverType','BOTH'] ])



### Shared Library 
temp=AdminConfig.list('Library')
myliblist=temp.split("\n")
for e in myliblist:
  if "mySharedLibrary" in e:
    AdminConfig.remove(e)
    print("Deleting existing shared library")
n1 = AdminConfig.getid('/Cell:'+cellName)
mylibrary = AdminConfig.create('Library', n1, [['name', 'mySharedLibrary'], ['classPath', 'c:/mySharedLibraryClasspath']])


### Link shared library to the server
appServer = AdminConfig.list('ApplicationServer', serv)
classLoader1 = AdminConfig.create('Classloader', appServer, [['mode',  'PARENT_LAST']])
AdminConfig.create('LibraryRef', classLoader1, [['libraryName', 'mySharedLibrary']])

### Create cluster
try:
  AdminTask.deleteCluster(['-clusterName', 'cluster1'])
  print("Deleting existing cluster")
except:
  print("Cluster not exist")
AdminConfig.convertToCluster(serv, 'cluster1')


### Save
AdminConfig.save()
#AdminNodeManagement.syncActiveNodes()
