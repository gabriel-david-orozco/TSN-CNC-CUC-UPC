import requests
import json
from pprint import pprint

device = {
   "ip": "172.17.0.2",
   "username": "admin",
   "password": "admin",
   "port": "8181",
}

headers = {
      #"Accept" : "application/yang-data+json",
      "Accept" : "*/*",
      "Content-Type" : "application/yang-data+json",
   }

module = "ietf-interfaces:interfaces"

# Remember to modify the node automatically
# http://192.168.0.41:8182/restconf/config/network-topology:network-topology/topology/topology-netconf/node/netopeer/yang-ext:mount/ietf-interfaces:interfaces

url = f"http://{device['ip']}:{device['port']}/restconf/config/network-topology:network-topology/topology/topology-netconf/node/TSN-switch2/yang-ext:mount/{module}/interface/PORT_0"

requests.packages.urllib3.disable_warnings()
response = requests.get(url, headers=headers, auth=(device['username'], device['password']), verify=False).json()


print('testing response')
print(response)
# interfaces = response['ietf-interfaces:interfaces']['interface']
#
# for interface in interfaces:
#    if bool(interface['ietf-ip:ipv4']): ## check if IP address is available
#       print(f"{interface['name']} -- {interface['description']} -- {interface['ietf-ip:ipv4']['address'][0]['ip']}")
