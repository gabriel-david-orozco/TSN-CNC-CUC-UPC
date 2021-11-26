import pika

from Djikstra_Path_Calculator import *
from Preprocessing import *

"""
This code should receive as input:

-------------- For the djikstra --------------
Adjacency_Matrix (rand_net)
Network_nodes (rand_net)
Stream_Source_Destination (rand_net) This value has to be regard as it is not properly from the rand net
Network_links (rand_net)

-------------- For the preprocessing --------------

Network_links (rand network)
Link_order_Descriptor (djikstra)
Number_of_streams (rand stream parameters)
max_frames (rand stream parameters)
Network_links (rand network)
Frames_per_Stream (ran stream parameters)
Streams_Period (ran stream parameters)
hyperperiod (ran stream parameters)

-------------- For the preprocessing --------------

This file call the functions created in Djikstra.py and Preprocessing.py and ensures communication ussing the 
rabbitMQ microservice. For the each external microservices exists a rabbitMQ queue for sending/receiving a Json file


Input parameters
┌────────────────────────────────────┬────────────────────────────────────┐
│  Information in the Jet_pre queue  │ Information in the Top_pre queue   │
│    Stream_Source_Destination       │   Adjacency_Matrix (rand_net)      │
│    Number_of_streams               │   Network_nodes (rand_net)         │
│    Max_frames                      │   Network_links (rand_net)         │
│    Frames_per_Stream               │                                    │
│    Streams_Period                  │                                    │
│    hyperperiod                     │                                    │
└────────────────────────────────────┴────────────────────────────────────┘
Output parameters
┌───────────────────────────────────┐
│  Information in the pre_ilp queue │
│      Number_of_Streams            │
│      Network_links                │
│      Link_order_Descriptor        │
│      Streams_Period               │
│      Hyperperiod                  │
│      Frames_per_Stream            │
│      Max_frames                   │
│      Num_of_Frames                │
│      Model_Descriptor             │
│      Model_Descriptor_vector      │
│      Deathline_Stream             │
│      Repetitions                  │
│      Repetitions_Descriptor       │
│      Unused_links                 │
│      Frame_Duration               │
│                                   │
└───────────────────────────────────┘



┌──────────────┐       Preprocessing Microservice
│ Jetconf      │   ┌────────────────────────────────┐
│ Microservice │   │                                │
└──────┬───────┘   │ ┌────────────────────────────┐ │   ┌───────────────────┐
       │           │ │                            │ │   │ ILP               │
       │           │ │ Djikstra.py                │ │   │    Calculator     │
       └──────────►│ │                            │ │   └───────────────────┘
    Jet_pre queue  │ │                            │ │             ▲
                   │ └────────────────────────────┘ │             │
                   │                                ├─────────────┘
                   │ ┌────────────────────────────┐ │   pre_ilp queue
    Top_pre queue  │ │                            │ │
       ┌──────────►│ │ Preprocessing.py           │ │
       │           │ │                            │ │
       │           │ │                            │ │
┌──────┴───────┐   │ └────────────────────────────┘ │
│ Topology     │   │                                │
│ Discovery    │   └────────────────────────────────┘
└──────────────┘
                            xxxxxxxxxxxxxxxx
                           x  RabbitMQ      x
                           x      Queues    x
                            xxxxxxxxxxxxxxxx


"""


# Connecting and declaring the rabbitmq channel for the jet_pre queueue

import os



if __name__ == "__main__":
    
    topo_flag = os.path.exists('/var/topology.txt')
    jetconf_flag = os.path.exists  ('/var/jetconf.txt')
    
    print(topo_flag,jetconf_flag)