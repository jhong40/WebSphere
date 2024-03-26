# /u01/app/WebSphere/ND/profiles/Dmgr01/bin/wsadmin.sh -f setclusterjvmprop.py CUSWCluster propkey propvalue

# Usage: wsadmin -f addJvmProperty.py [node:]server property value [description]
# e.g. wsadmin -f addJvmProperty.py all property value
# e.g. wsadmin -f addJvmProperty.py myNode:myServer property value
# e.g. wsadmin -f addJvmProperty.py myServer property value

#### clustername -> jvm name ########
cluster_name = sys.argv[0]
serverlist=[]
cluster_conf_id = AdminConfig.getid("/ServerCluster:"+cluster_name )
if not cluster_conf_id:
  raise "Cluster %s does not exist!" % cluster_name

member_conf_ids = AdminConfig.showAttribute(cluster_conf_id, "members")
member_conf_ids = member_conf_ids[1:-1]
for member_conf_id in member_conf_ids.split():
  member_name=AdminConfig.showAttribute(member_conf_id, "memberName")
  node_name=AdminConfig.showAttribute(member_conf_id, "nodeName")
  serverlist.append(node_name+":"+member_name)

#### for each jvm, set the prop value ########
for server in serverlist:
  #print(server)

  #server = sys.argv[0]
  property = sys.argv[1]
  value = sys.argv[2]
  if (len(sys.argv) == 4):
      descr = sys.argv[3]
  else :
        descr = None

  # Convert a list of items separated by linefeeds into an array
  def getListArray(l):
      return l.splitlines()

  # Obtain the "simple" server name
  def getServerName(s):
      return AdminConfig.showAttribute(s, 'name')

  # Add common attr list to specified Server's JVM
  def addPropertiesToServer(s):
      jvm = AdminConfig.list('JavaVirtualMachine', s)

      # Look for existing property so we can replace it (by removing it first)
      currentProps = getListArray(AdminConfig.list("Property", jvm))
      for prop in currentProps:
          if property == AdminConfig.showAttribute(prop, "name"):
              print "Removing existing property from Server %s" % s
              AdminConfig.remove(prop)

      # Store new property in 'systemProperties' object
      print "Adding property to Server %s" % s
      AdminConfig.modify(jvm,[['systemProperties',attr]])

  # Construct list with new property name and value
  attr = []

  if (descr is None):
      print "Adding property %s=%s" % (property,value)
      attr.append([['name',property],['value',value]])
  else:
      print "Adding property %s=%s,%s" % (property,value,descr)
      attr.append([['name',property],['value',value],['description',descr]])

  # Locate all Application Servers if server is 'all'
  if (server == 'all'):
      servers = AdminConfig.list('Server')
      for aServer in getListArray(servers):
          type = AdminConfig.showAttribute(aServer,'serverType')
          if (type == 'APPLICATION_SERVER'):
              addPropertiesToServer(aServer)
  # TODO: support comma-separated list of servers

  else:
      # See if node:server specified
      colon = server.find(':')
      if (colon != -1) :
          node = server[:colon]
          server = server[colon+1:]
          print "Locating Server %s on Node %s" % (server,node)
          servers = AdminConfig.getid('/Node:'+node+'/Server:'+server+'/')

      # Locate specified Server and its JVM
      else :
          servers = AdminConfig.getid('/Server:'+server+'/')

      # servers could be a list of servers, all with the same name
      if servers :
          for s in servers.splitlines() :
              addPropertiesToServer(s)
      else :
          print "Specified server not found"

  # Save changes
  if (AdminConfig.hasChanges()):
      AdminConfig.save()


#### ripple start cluster ########
print("Ripple restart Cluster")
cellName = AdminControl.getCell()
clusterName = cluster_name

#print(cellName)
#print(clusterName)

clusterMgr = AdminControl.completeObjectName("cell=" + cellName + ",type=ClusterMgr,*")
AdminControl.invoke(clusterMgr, 'retrieveClusters')
cluster = AdminControl.completeObjectName("cell=" + cellName + ",type=Cluster,name=" + clusterName + ",*")
AdminControl.invoke(cluster, 'rippleStart')



import time
import datetime


clustername=clusterName
clusterbean=cluster

timeout=time.time()+60*5
i=0;
while True:
  time.sleep(2)
  i=i+1
  timelapse=i*5
  status=AdminControl.getAttribute(clusterbean, 'state')

  now=datetime.datetime.now()
  nowstr="%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)

  print(nowstr+" "+clustername+" Status: " + status + " " + str(timelapse) + " sec")
  if status.find('running')!=-1:
    print "----" + clustername+" Started....."
    break
  if time.time()>timeout:
    print "----Warning " + clustername+" Ripplestart Timeout..."
    break
