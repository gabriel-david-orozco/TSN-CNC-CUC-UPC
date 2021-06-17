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
        mac_address = "8c-c3-C1-1f-75-E4"
        interface_name = "8c-c3-C1-1f-75-E4"
        index = 1
        destination_mac_addres = "8c-c3-C1-1f-75-E4"
        source_mac_address = "8c-c3-C1-1f-75-E4"
        status_info = {}
        payload= {
            "status-info": {
                "talker-status" : talker_status,
                "listener-status" : "1",
                "failure-code" : 0
                },
            "status-info": status_info,
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
                    ],

                }

                }
        }
        json_string = json.dumps(payload)
        print(payload)
        print("looking for this",type(json_string))
        return payload # empty

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info

# Instantiate state data handlers
def register_state_handlers(ds: BaseDatastore):
    configuration = CNC_RestconfStateHandler_configuration(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration")
    ds.handlers.state.register(configuration)
