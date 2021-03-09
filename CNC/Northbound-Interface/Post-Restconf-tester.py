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
      "Accept" : "*/*",
      "Content-Type" : "application/yang-data+json",
   }

module = "ietf-interfaces:interfaces"

url = f"http://{device['ip']}:{device['port']}/restconf/config/network-topology:network-topology/topology/topology-netconf/node/netopeer/yang-ext:mount/{module}"

payload = {
   "interface": [
    {
      "name": "Loopback10000",
      "description": "Adding loopback10000",
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
response = requests.post(url, headers=headers, data=json.dumps(payload), auth=(device['username'], device['password']), verify=False)

if (response.status_code == 201):
   print("Successfully added interface")
else:
   print("Issue with adding interface")
