from colorlog import info

from yangson.instance import InstanceRoute

from jetconf.helpers import JsonNodeT, PathFormat
from jetconf.handler_base import StateDataContainerHandler
from jetconf.data import BaseDatastore
import json

# ---------- User-defined handlers follow ----------

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration
class CNC_RestconfStateHandler_configuration(StateDataContainerHandler):
    def generate_node(self, node_ii: InstanceRoute, username: str, staging: bool) -> JsonNodeT:
        talker_status = "1"
        mac_address_ii = self.ds.parse_ii("ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list=8c-c3-C1-1f-75-E4:5E-b3/request/talker/end-station-interfaces=60-F2-62-74-45-F0,eth0/mac-address", PathFormat.URL)
        mac_address = self.ds.get_data_root().goto(mac_address_ii).value
        testing_ii = self.ds.parse_ii("ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list", PathFormat.URL)
        testing = self.ds.get_data_root().goto(testing_ii).value

        for test in testing :
            print("tipo de la variable",test)
            print("tipo de la variable",type(test))
        #print("testing, just for fun", testing)
        print("the type of the variable", type(testing))
        #print("testing, just for fun, parsed data", testing_ii)
        print("the type of the variable, parsed data", type(testing_ii))
        #mac_address = "8c-c3-C1-1f-75-E4"
        interface_name = "8c-c3-C1-1f-75-E4"
        index = 1
        destination_mac_addres = "8c-c3-C1-1f-75-E4"
        source_mac_address = "8c-c3-C1-1f-75-E4"
        failed_interfaces = {}
        flag=1
        if flag == 1 :
             failed_interfaces = {
                "mac-address" : mac_address,
                "interface-name" : interface_name
             }
        payload= {
            "status-info": {
                "talker-status" : talker_status,
                "listener-status" : "1",
                "failure-code" : 0
                },
            "failed-interfaces": [failed_interfaces],
            "talker": {
                "accumulated-latency" : 100,
                "interface-configuration" : {
                    "interface-list" : [
                        {
                        "mac-address" : mac_address,
                        "interface-name" : interface_name,
                        "config-list" : [
                            {
                            "index" : index,
                            "ieee802-mac-addresses" : {
                                "destination-mac-address" : destination_mac_addres,
                                "source-mac-address" : source_mac_address
                                },
                            "time-aware-offset" : 100
                            }
                            ]
                        }
                    ]
                }
                },
            "listener-list" : [
            {
            "index" : index,
            "accumulated-latency" : 100,
            "interface-configuration" : {
                "interface-list" : [
                    {
                    "mac-address" : mac_address,
                    "interface-name" : interface_name,
                    "config-list" : [
                        {
                        "index" : index,
                        "ieee802-mac-addresses" : {
                            "destination-mac-address" : destination_mac_addres,
                            "source-mac-address" : source_mac_address
                            },
                        "time-aware-offset" : 100
                        }
                        ]
                    }
                ]
            }
            }
            ]
        }
        json_string = json.dumps(payload)
        #print(payload)
        print("looking for this",type(json_string))
        return payload # empty

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info

# Instantiate state data handlers
def register_state_handlers(ds: BaseDatastore):
    configuration = CNC_RestconfStateHandler_configuration(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration")
    ds.handlers.state.register(configuration)
