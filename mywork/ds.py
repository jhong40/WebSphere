# has issue with j2c alias 

dsname='dsaaa'
dsjndi='jdbc/jndiaaa'
dburl='jdbc:oracle:thin:@//aaa:1532/bbb'
dbscope='Cluster=cluster1'

## Delete exisint JDBC Driver, J2C alias

print("Deleting JDBC Driver if exist")
dbproviders=AdminTask.listJDBCProviders('-scope '+dbscope)
x=dbproviders.split("\n")
for y in x:
  if "MY" in y:
    print(y)
    print("  Found one JDBC, deleting now") 
    AdminTask.deleteJDBCProvider(y)

print("Deleting J2C alias if exist")
j2cNames = AdminTask.listAuthDataEntries()
for j2cEntry in j2cNames.splitlines():
 if(j2cEntry.find('zzz') > -1):
   myalias=j2cEntry.split(" ")[1].split("]")[0]
   print("Found zzz alias, deleting...")
   print(myalias)
   AdminTask.deleteAuthDataEntry('-alias '+myalias)


### Create J2C alias
print("Creating J2C Alias")
a=AdminTask.createAuthDataEntry(['-alias', 'zzz', '-user', 'myuser', '-password', 'mypass'])
myj2c=AdminConfig.showAttribute(a,'alias')
print(myj2c)
AdminConfig.save()

###############################################
#myj2c='blahcellmanager01/bbbb' 
###############################################

## Create jdbc driver
print("Create JDBC Driver, and DS")
dr=AdminTask.createJDBCProvider('[-scope '+ dbscope + ' -databaseType Oracle -providerType "Oracle JDBC Driver" -implementationType "Connection pool data source" -name "MY Oracle JDBC Driver" -description "My Oracle JDBC" -classpath [/u01/app/WebSphere/AppServer/jdbcdrivers/ojdbc8.jar ] -nativePath "" ]')

## Create datasource 
ds=AdminTask.createDatasource(dr, '[-name '+dsname+' -jndiName '+dsjndi+' -dataStoreHelperClassName com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias '+myj2c+' -configureResourceProperties [[URL java.lang.String '+dburl+']]]')

AdminConfig.create('MappingModule', ds, '[[authDataAlias '+ myj2c + '] [mappingConfigAlias DefaultPrincipalMapping]]')

## for CMP, need to make change on CMP Conn Factory additionally
a=AdminConfig.list('CMPConnectorFactory')
cmp_cf=a.split("\n")
cmpid=""
for e in cmp_cf:
  if AdminConfig.showAttribute(e,'cmpDatasource')==ds: 
    cmpid=e
    #print(e)
AdminConfig.modify(cmpid, '[[authDataAlias "'+myj2c+'"] [xaRecoveryAuthAlias ""]]')
AdminConfig.create('MappingModule', cmpid, '[[authDataAlias '+myj2c+'] [mappingConfigAlias DefaultPrincipalMapping]]')



## Change the Datasource Custom Properties

#ds = AdminConfig.getid('/ServerCluster:CUSWCluster/JDBCProvider:"MY Oracle JDBC Driver"/DataSource:dsaaa/')
#print(ds)
propSet = AdminConfig.showAttribute(ds, 'propertySet')
a=AdminConfig.showAttribute(propSet, 'resourceProperties')
b=a.strip('[]')
c=b.split(" ")

mydict =	{
  "driverType": "thin",
  "databaseName": "ddd",
  "serverName": "dbserver", 
  "portNumber": "1521",
  "loginTimeout": "0",
  "description": "Datasource description", 
  "webSphereDefaultIsolationLevel": "2" 
}

for e in c:
  for myn, myv in mydict.items():
    if AdminConfig.showAttribute(e,'name') == myn: 
      value=['value',myv]
      rpAttrs = [value]
      AdminConfig.modify(e, rpAttrs)
      att=AdminConfig.showall(e)
      #print(att)
 
## Delete the rest of Datasource Properties
for e in c:
  flag=0
  for myn in mydict.keys():
    if AdminConfig.showAttribute(e,'name') == myn: 
      flag=1
  if flag==0:
    AdminConfig.remove(e)
  
## Change the Datasource Connection Pool size

AdminConfig.modify(ds, '[[statementCacheSize "500"]]')
AdminConfig.modify(ds, '[[connectionPool [[connectionTimeout 75]  [maxConnections 55] [minConnections 5] [reapTime 180] [unusedTimeout 360] [agedTimeout 1080] ]]]')
#print(AdminConfig.showall(ds))


AdminConfig.save()
AdminNodeManagement.syncActiveNodes()

