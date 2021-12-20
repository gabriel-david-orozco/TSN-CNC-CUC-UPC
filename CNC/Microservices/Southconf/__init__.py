
'''
This microservice is in charge of sending the appropiate configuration to the two Southbound Microservices i.e., Vlan_Configurator and Opendaylight

The Opendaylight controller will receive a HTTP jetconf for each of the elements in the topology following the ieee802dot1sched.

IP address -> Table between the node number and an IP address
interface.name ->Table between the connection and the interface name 
gate-enabled -> Always on
admin-gate-states -> 255 (everything on)
admin-control-list-length -> This should vary according to the number of streams will pass through the switch
admin-control-list - > one per each stream
operation-name: set-gates-states 
sgs-params
gate-states-value -> This is a value in binary to decimal that shold represent the state of the gate for that specific traffic
time-interval-value -> Total duration of the stream
admin-cycle-time -> This is just one cause is the general of the gate, numerator and denominator for representing the total time
admin-cycle-time-extension -> same as above
admin-base-time -> seconds and fractionals
seconds
fractional-seconds
config-change -> Always true

On the other hand, VLan configurator will need the following parameters:

IP address ->
VLANS and priority coddes
Topology
Members of the same Vlan

This is the diagram that represents this microservice:

                            Export
                                 Service

                                  ▲
                                  │
        ┌─────────────────────────┼────────────────────────────┐
        │                         │                            │
        │  ┌────────────┐   ┌─────┴──────┐    ┌────────────┐   │
        │  │            │   │            │    │            │   │    ┌──────────────┐
        │  │ ilp_south  │   │ Web        │    │ Json vlans │   │    │              │
   ┌────┼──► Rabitmq    │   │  Interface │    │            │   │    │  Vlan        │
   │    │  │            │   │            │    │ contains:  ├───┼────►  Configurator│
┌──┴──┐ │  └─────┬──────┘   └────────────┘    │ -devices   │   │    │              │
│ ILP │ │        │                            │ -vlans each│   │    │              │
└─────┘ │  ┌─────▼─────────────────────────┐  │            │   │    └──────────────┘
        │  │                               │  │            │   │
        │  │ ConfGen              ┌────────┼──►            │   │
        │  │                      │        │  └────────────┘   │
        │  │  ┌───────────────────┴─────┐  │                   │
        │  │  │ Vlans_configurator      │  │  ┌────────────┐   │
        │  │  │                         │  │  │ Restconf   │   │    ┌──────────────┐
        │  │  └─────────────────────────┘  │  │            │   │    │              │
        │  │                               │  │ contains:  │   │    │  Open        │
        │  │  ┌─────────────────────────┐  │  │ -devices   ├───┼────►    Daylight  │
        │  │  │ TAS_configurator        │  │  │ -offsets   │   │    │              │
        │  │  │                         ├──┼──► -priorities│   │    │              │
        │  │  └─────────────────────────┘  │  │ -cycles    │   │    └──────────────┘
        │  │                               │  │            │   │
        │  └───────────────────────────────┘  └────────────┘   │
        │                                                      │
        └──────────────────────────────────────────────────────┘
'''


