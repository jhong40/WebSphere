##### Ceate SIB and related JMS resources

try: 
  AdminTask.deleteSIBus('[-bus bus1 ]') 
  print("deleted bus1")
except:
  print("bus1 not existing")

## Create Bus
AdminTask.createSIBus('[-bus bus1 -description [A new bus] -busSecurity false ]')

## Add Bus member
AdminTask.addSIBusMember('[-bus bus1 -cluster cluster1 -enableAssistance true -policyName SCALABILITY_HA -fileStore -logSize 100 -logDirectory logs/SiBus -permanentStoreDirectory logs/Sibus -temporaryStoreDirectory logs/Sibus ]') 

## Create Bus Destination
AdminTask.createSIBDestination("[-bus bus1 -name bbb -type QUEUE -cluster cluster1]")


## Create JMS Queque 
clusterid=AdminConfig.getid("/ServerCluster:cluster1" )
AdminTask.createSIBJMSQueue(clusterid, ["-name", "MyJMSQueue", "-jndiName", "MyJMSQueue", "-busName bus1", "-queueName", "bbb", "-deliveryMode", "Application", "-readAhead", "AsConnection", "-producerBind", "FALSE"])


## Create JMS Connection Factory 
confactory=AdminTask.createSIBJMSConnectionFactory(clusterid, ["-name", "MyConfactory", "-jndiName", "jms/myjmscf1", "-busName", "bus1"])
print(confactory)

## Change JMS Connection Factory Connection Pool size
AdminConfig.modify(confactory, '[[connectionPool [[connectionTimeout 180]  [maxConnections 300] [minConnections 10] [reapTime 180] [unusedTimeout 1800] [agedTimeout 0] ]]]')


AdminConfig.save()

