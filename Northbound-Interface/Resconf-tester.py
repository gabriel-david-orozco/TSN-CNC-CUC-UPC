import requests
import json
from pprint import pprint

device = {
   "ip": "192.168.0.41",
   "username": "admin",
   "password": "admin",
   "port": "8182",
}

headers = {
      "Accept" : "application/yang-data+json",
      "Content-Type" : "application/yang-data+json",
   }

module = "ietf-interfaces:interfaces"

# Remember to modify the node automatically
# http://192.168.0.41:8182/restconf/config/network-topology:network-topology/topology/topology-netconf/node/netopeer/yang-ext:mount/ietf-interfaces:interfaces

url = f"http://{device['ip']}:{device['port']}/restconf/config/network-topology:network-topology/topology/topology-netconf/node/netopeer/yang-ext:mount/{module}"

requests.packages.urllib3.disable_warnings()
response = requests.get(url, headers=headers, auth=(device['username'], device['password']), verify=False)


print('testing response')
print(response)
interfaces = response['ietf-interfaces:interfaces']['interface']

for interface in interfaces:
   if bool(interface['ietf-ip:ipv4']): ## check if IP address is available
      print(f"{interface['name']} -- {interface['description']} -- {interface['ietf-ip:ipv4']['address'][0]['ip']}")
