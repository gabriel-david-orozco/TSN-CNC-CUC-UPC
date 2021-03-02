#This code is for testing the API integration in the northbound interface

import requests

resp = requests.get('http://192.168.0.41:8182/restconf/operational/network-topology:network-topology/topology/topology-netconf/node/netopeer/yang-ext:mount/ietf-interfaces:interfaces')
if resp.status_code != 200:
    # This means something went wrong.
    #raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    raise print("Not working")
for todo_item in resp.json():
    print('{} {}'.format(todo_item['id'], todo_item['summary']))
