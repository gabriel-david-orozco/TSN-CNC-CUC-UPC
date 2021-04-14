# YANG Modules description

For the communication between the CNC and the CUC in the fully-centralized architecture we used as base the Yang module defined in the 802.1Qcc IEEE standard chapter 46.3.1. However, that yang module only specifies the groups and typedefs and not the full yang module. The IEEE TSN task group is woking in standarize that Yang model in the 802.1qdj amendment.

Thats the reason of why we create our own YANG model based on the groups and typedefs of the 802.1Qcc

The module is allocated on the ieee802-dot1q-tsn-types-upc-version@2018-02-15.yang file, and its tree structure is as follows:

```
module: ieee802-dot1q-tsn-types-upc-version
  +--rw tsn-uni
     +--rw stream-list* [stream-id]
     |  +--rw stream-id        stream-id-type
     |  +--rw request
     |  |  +--rw talker
     |  |  |     uses group-talker
     |  |  +--rw listeners-list* [index]
     |  |  |     uses group-listener
     |  |  +---x compute-request
     |  +--ro configuration
     |     |     uses group-status-stream
     |     +--ro talker
     |     |     uses group-talker
     |     +--ro listener-list* [index]
     |     |     uses group-listener
     |     +---x deploy-configuration
     |     +---x undeploy-configuration
     |     +---x delete-configuration
     +---x compute-all-configuration
     +---x deploy-all-configuration
     +---x undeploy-all-configuration
     +---x delete-all-configuration
```
Complete module description using pyang

```
module: ieee802-dot1q-tsn-types-upc-version
  +--rw tsn-uni
     +--rw stream-list* [stream-id]
     |  +--rw stream-id        stream-id-type
     |  +--rw request
     |  |  +--rw talker
     |  |  |  +--rw stream-rank
     |  |  |  |  +--rw rank?   uint8
     |  |  |  +--rw end-station-interfaces* [mac-address interface-name]
     |  |  |  |  +--rw mac-address       string
     |  |  |  |  +--rw interface-name    string
     |  |  |  +--rw data-frame-specification* [index]
     |  |  |  |  +--rw index                          uint8
     |  |  |  |  +--rw (field)?
     |  |  |  |     +--:(ieee802-mac-addresses)
     |  |  |  |     |  +--rw ieee802-mac-addresses
     |  |  |  |     |     +--rw destination-mac-address?   string
     |  |  |  |     |     +--rw source-mac-address?        string
     |  |  |  |     +--:(ieee802-vlan-tag)
     |  |  |  |     |  +--rw ieee802-vlan-tag
     |  |  |  |     |     +--rw priority-code-point?   uint8
     |  |  |  |     |     +--rw vlan-id?               uint16
     |  |  |  |     +--:(ipv4-tuple)
     |  |  |  |     |  +--rw ipv4-tuple
     |  |  |  |     |     +--rw source-ip-address?        inet:ipv4-address
     |  |  |  |     |     +--rw destination-ip-address?   inet:ipv4-address
     |  |  |  |     |     +--rw dscp?                     uint8
     |  |  |  |     |     +--rw protocol?                 uint16
     |  |  |  |     |     +--rw source-port?              uint16
     |  |  |  |     |     +--rw destination-port?         uint16
     |  |  |  |     +--:(ipv6-tuple)
     |  |  |  |        +--rw ipv6-tuple
     |  |  |  |           +--rw source-ip-address?        inet:ipv6-address
     |  |  |  |           +--rw destination-ip-address?   inet:ipv6-address
     |  |  |  |           +--rw dscp?                     uint8
     |  |  |  |           +--rw protocol?                 uint16
     |  |  |  |           +--rw source-port?              uint16
     |  |  |  |           +--rw destination-port?         uint16
     |  |  |  +--rw traffic-specification
     |  |  |  |  +--rw interval
     |  |  |  |  |  +--rw numerator?     uint32
     |  |  |  |  |  +--rw denominator?   uint32
     |  |  |  |  +--rw max-frames-per-interval?   uint16
     |  |  |  |  +--rw max-frame-size?            uint16
     |  |  |  |  +--rw transmission-selection?    uint8
     |  |  |  |  +--rw time-aware!
     |  |  |  |     +--rw earliest-transmit-offset?   uint32
     |  |  |  |     +--rw latest-transmit-offset?     uint32
     |  |  |  |     +--rw jitter?                     uint32
     |  |  |  +--rw user-to-network-requirements
     |  |  |  |  +--rw num-seamless-trees?   uint8
     |  |  |  |  +--rw max-latency?          uint32
     |  |  |  +--rw interface-capabilities
     |  |  |     +--rw vlan-tag-capable?           boolean
     |  |  |     +--rw cb-stream-iden-type-list*   uint32
     |  |  |     +--rw cb-sequence-type-list*      uint32
     |  |  +--rw listeners-list* [index]
     |  |  |  +--rw index                           uint16
     |  |  |  +--rw end-station-interfaces* [mac-address interface-name]
     |  |  |  |  +--rw mac-address       string
     |  |  |  |  +--rw interface-name    string
     |  |  |  +--rw user-to-network-requirements
     |  |  |  |  +--rw num-seamless-trees?   uint8
     |  |  |  |  +--rw max-latency?          uint32
     |  |  |  +--rw interface-capabilities
     |  |  |     +--rw vlan-tag-capable?           boolean
     |  |  |     +--rw cb-stream-iden-type-list*   uint32
     |  |  |     +--rw cb-sequence-type-list*      uint32
     |  |  +---x compute-request
     |  +--ro configuration
     |     +--ro status-info
     |     |  +--ro talker-status?     enumeration
     |     |  +--ro listener-status?   enumeration
     |     |  +--ro failure-code?      uint8
     |     +--ro failed-interfaces* [mac-address interface-name]
     |     |  +--ro mac-address       string
     |     |  +--ro interface-name    string
     |     +--ro talker
     |     |  +--ro accumulated-latency?       uint32
     |     |  +--ro interface-configuration
     |     |     +--ro interface-list* [mac-address interface-name]
     |     |        +--ro mac-address       string
     |     |        +--ro interface-name    string
     |     |        +--ro config-list* [index]
     |     |           +--ro index                          uint8
     |     |           +--ro (config-value)?
     |     |              +--:(ieee802-mac-addresses)
     |     |              |  +--ro ieee802-mac-addresses
     |     |              |     +--ro destination-mac-address?   string
     |     |              |     +--ro source-mac-address?        string
     |     |              +--:(ieee802-vlan-tag)
     |     |              |  +--ro ieee802-vlan-tag
     |     |              |     +--ro priority-code-point?   uint8
     |     |              |     +--ro vlan-id?               uint16
     |     |              +--:(ipv4-tuple)
     |     |              |  +--ro ipv4-tuple
     |     |              |     +--ro source-ip-address?        inet:ipv4-address
     |     |              |     +--ro destination-ip-address?   inet:ipv4-address
     |     |              |     +--ro dscp?                     uint8
     |     |              |     +--ro protocol?                 uint16
     |     |              |     +--ro source-port?              uint16
     |     |              |     +--ro destination-port?         uint16
     |     |              +--:(ipv6-tuple)
     |     |              |  +--ro ipv6-tuple
     |     |              |     +--ro source-ip-address?        inet:ipv6-address
     |     |              |     +--ro destination-ip-address?   inet:ipv6-address
     |     |              |     +--ro dscp?                     uint8
     |     |              |     +--ro protocol?                 uint16
     |     |              |     +--ro source-port?              uint16
     |     |              |     +--ro destination-port?         uint16
     |     |              +--:(time-aware-offset)
     |     |                 +--ro time-aware-offset?       uint32
     |     +--ro listener-list* [index]
     |     |  +--ro index                      uint16
     |     |  +--ro accumulated-latency?       uint32
     |     |  +--ro interface-configuration
     |     |     +--ro interface-list* [mac-address interface-name]
     |     |        +--ro mac-address       string
     |     |        +--ro interface-name    string
     |     |        +--ro config-list* [index]
     |     |           +--ro index                          uint8
     |     |           +--ro (config-value)?
     |     |              +--:(ieee802-mac-addresses)
     |     |              |  +--ro ieee802-mac-addresses
     |     |              |     +--ro destination-mac-address?   string
     |     |              |     +--ro source-mac-address?        string
     |     |              +--:(ieee802-vlan-tag)
     |     |              |  +--ro ieee802-vlan-tag
     |     |              |     +--ro priority-code-point?   uint8
     |     |              |     +--ro vlan-id?               uint16
     |     |              +--:(ipv4-tuple)
     |     |              |  +--ro ipv4-tuple
     |     |              |     +--ro source-ip-address?        inet:ipv4-address
     |     |              |     +--ro destination-ip-address?   inet:ipv4-address
     |     |              |     +--ro dscp?                     uint8
     |     |              |     +--ro protocol?                 uint16
     |     |              |     +--ro source-port?              uint16
     |     |              |     +--ro destination-port?         uint16
     |     |              +--:(ipv6-tuple)
     |     |              |  +--ro ipv6-tuple
     |     |              |     +--ro source-ip-address?        inet:ipv6-address
     |     |              |     +--ro destination-ip-address?   inet:ipv6-address
     |     |              |     +--ro dscp?                     uint8
     |     |              |     +--ro protocol?                 uint16
     |     |              |     +--ro source-port?              uint16
     |     |              |     +--ro destination-port?         uint16
     |     |              +--:(time-aware-offset)
     |     |                 +--ro time-aware-offset?       uint32
     |     +---x deploy-configuration
     |     +---x undeploy-configuration
     |     +---x delete-configuration
     +---x compute-all-configuration
     +---x deploy-all-configuration
     +---x undeploy-all-configuration
     +---x delete-all-configuration
```
# YANG Modules description

For the moment, the operational data is not ready since it has to be delivered at the end of the controlling process. Consequently, a draft version of the Yang model without the actions and read-only data has been provided. The three structure is as follows:

```
module: ieee802-dot1q-tsn-types-upc-version
  +--rw tsn-uni
     +--rw stream-list* [stream-id]
        +--rw stream-id        stream-id-type
        +--rw request
        |  +--rw talker
        |  |     ...
        |  +--rw listeners-list* [index]
        |        ...
        +--ro configuration
           +--ro status-info
           |     ...
           +--ro failed-interfaces* [mac-address interface-name]
           |     ...
           +--ro talker
           |     ...
           +--ro listener-list* [index]
           
```
