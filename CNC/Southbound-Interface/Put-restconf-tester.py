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
      "Content-Type" : "application/json",
   }

module = "ietf-interfaces:interfaces"

# Remember to add the name of the interface when you discover what is the issue with the put method
url = f"http://{device['ip']}:{device['port']}/restconf/config/network-topology:network-topology/topology/topology-netconf/node/TSN-switch2/yang-ext:mount/{module}/interface/PORT_0"

payload = {
    "interface": [
        {
            "name": "PORT_0",
            "ieee802-dot1q-bridge:bridge-port": {},
            "type": "iana-if-type:ethernetCsmacd",
            "ieee802-dot1q-sched:gate-parameters": {
                "admin-gate-states": "255",
                "gate-enabled": "false",
                "admin-control-list-length": "0",
                "config-change": "false",
                "admin-cycle-time": {
                    "numerator": "1",
                    "denominator": "1000"
                },
                "admin-base-time": {
                    "seconds": "0",
                    "fractional-seconds": "0"
                },
                "admin-cycle-time-extension": "0"
            }
        }
    ]
}
requests.packages.urllib3.disable_warnings()
response = requests.put(url, headers=headers, json=payload, auth=(device['username'], device['password']), verify=False)
print(response)
if (response.status_code == 204):
   print("Successfully updated interface")
else:
   print("Issue with updating interface")
