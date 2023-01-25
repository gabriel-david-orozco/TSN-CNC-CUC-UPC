from colorlog import info
from typing import List, Dict, Union, Any

from yangson.instance import InstanceRoute
from jetconf.data import BaseDatastore, DataChange
from jetconf.helpers import ErrorHelpers, LogHelpers
from jetconf.handler_base import ConfDataListHandler
from jetconf.handler_base import ConfDataObjectHandler

JsonNodeT = Union[Dict[str, Any], List]
epretty = ErrorHelpers.epretty
debug_confh = LogHelpers.create_module_dbg_logger(__name__)


# ---------- User-defined handlers follow ----------



class CNC_RestconfConfHandler(ConfDataListHandler):
    def create_item(self, ii: InstanceRoute, ch: "DataChange"):
        debug_confh(self.__class__.__name__ + " replace triggered")
        info("___________________________Retrieving Infoooo___________________________")
        info("Creating item '/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list' in app configuration")

    def create_list(self, ii: InstanceRoute, ch: "DataChange"):
        debug_confh(self.__class__.__name__ + " replace triggered")
        info("___________________________Retrieving Infoooo___________________________")
        info("Creating list '/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list' in app configuration")

    def replace_item(self, ii: InstanceRoute, ch: "DataChange"):
        debug_confh(self.__class__.__name__ + " replace triggered")
        info("___________________________Retrieving Infoooo___________________________")
        info("Replacing item '/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list' in app configuration")

    def replace_list(self, ii: InstanceRoute, ch: "DataChange"):
        debug_confh(self.__class__.__name__ + " replace triggered")
        info("___________________________Retrieving Infoooo___________________________")
        info("Replacing list '/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list' in app configuration")

    def delete_item(self, ii: InstanceRoute, ch: "DataChange"):
        debug_confh(self.__class__.__name__ + " delete triggered")
        info("___________________________Retrieving Infoooo___________________________")
        info("Deleting item '/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list' from app configuration")

    def delete_list(self, ii: InstanceRoute, ch: "DataChange"):
        debug_confh(self.__class__.__name__ + " delete triggered")
        info("___________________________Retrieving Infoooo___________________________")
        info("Deleting list '/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list' from app configuration")


def register_conf_handlers(ds: BaseDatastore):
    ds.handlers.conf.register(CNC_RestconfConfHandler(ds, "/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list"))
