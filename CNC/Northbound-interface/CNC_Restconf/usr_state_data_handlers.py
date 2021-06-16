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

        payload= {
        "status-info": {
        "talker-status" : "1",
        "listener-status" : "1",
        "failure-code" : 0
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
