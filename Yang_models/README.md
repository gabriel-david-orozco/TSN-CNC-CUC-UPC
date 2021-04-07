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
