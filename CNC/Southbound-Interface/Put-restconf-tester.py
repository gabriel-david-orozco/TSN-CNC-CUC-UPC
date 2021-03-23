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
      #"Accept" : "application/yang-data+json",
      "Accept" : "*/*",
      "Content-Type" : "application/yang-data+json",
   }

module = "ietf-interfaces:interfaces"

# Remember to add the name of the interface when you discover what is the issue with the put method
url url = f"http://{device['ip']}:{device['port']}/restconf/config/network-topology:network-topology/topology/topology-netconf/node/netopeer/yang-ext:mount/{module}"

payload = {
   "interface": [
    {
      "name": "Loopback10000",
      "description": "Adding loopback10000 - changed",
      "type": "iana-if-type:softwareLoopback",
      "enabled": "true",
      "ietf-ip:ipv4": {
        "address": [
          {
            "ip": "192.0.2.60",
            "netmask": "255.255.255.255"
          }
        ]
      }
    }
  ]
 }
requests.packages.urllib3.disable_warnings()
response = requests.put(url, headers=headers, data=json.dumps(payload), auth=(device['username'], device['password']), verify=False)

if (response.status_code == 204):
   print("Successfully updated interface")
else:
   print("Issue with updating interface")
