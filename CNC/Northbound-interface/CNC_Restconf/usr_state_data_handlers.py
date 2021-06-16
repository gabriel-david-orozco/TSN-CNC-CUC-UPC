from colorlog import info

from yangson.instance import InstanceRoute

from jetconf.helpers import JsonNodeT, PathFormat
from jetconf.handler_base import StateDataContainerHandler
from jetconf.data import BaseDatastore


# ---------- User-defined handlers follow ----------

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration
class CNC_RestconfStateHandler_configuration(StateDataContainerHandler):
    def generate_node(self, node_ii: InstanceRoute, username: str, staging: bool) -> JsonNodeT:

        payload={
        "status-info": {
            "talker_status": "1",
            "listener_status": "2",
            "failure-code": "0"
            }
        }

        return payload # empty

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info
class CNC_RestconfStateHandler_configuration_status_info(StateDataContainerHandler):
    def generate_node(self, node_ii: InstanceRoute, username: str, staging: bool) -> JsonNodeT:
        return 1 # empty

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info/talker-status
class CNC_RestconfStateHandler_configuration_talker_status(StateDataContainerHandler):
    def generate_node(self, node_ii: InstanceRoute, username: str, staging: bool) -> JsonNodeT:
        return "1" # should be 1

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info/listener-status
class CNC_RestconfStateHandler_configuration_listener_status(StateDataContainerHandler):
    def generate_node(self, node_ii: InstanceRoute, username: str, staging: bool) -> JsonNodeT:

        return "2" # should be 1

# This handler will generate /ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info/failure-code
class CNC_RestconfStateHandler_configuration_failure_code(StateDataContainerHandler):
    def generate_node(self, node_ii: InstanceRoute, username: str, staging: bool) -> JsonNodeT:

        return 0 # should be 0



# Instantiate state data handlers
def register_state_handlers(ds: BaseDatastore):
    configuration = CNC_RestconfStateHandler_configuration(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration")
    #configuration_status_info = CNC_RestconfStateHandler_configuration_status_info(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info")
    #configuration_talker_status = CNC_RestconfStateHandler_configuration_talker_status(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info/talker-status")
    #configuration_listener_status = CNC_RestconfStateHandler_configuration_listener_status(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info/listener-status")
    #configuration_failure_code = CNC_RestconfStateHandler_configuration_failure_code(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list/configuration/status-info/failure-code")
    ds.handlers.state.register(configuration)
    #ds.handlers.state.register(configuration_status_info)
    #ds.handlers.state.register(configuration_talker_status)
    #ds.handlers.state.register(configuration_listener_status)
    #ds.handlers.state.register(configuration_failure_code)
