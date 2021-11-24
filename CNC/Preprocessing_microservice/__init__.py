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


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()



#Djikstra scheduler should be executed first
network = Network_Topology(Adjacency_Matrix) # Using the Network Topology class
all_paths_matrix = all_paths_matrix_generator(Network_nodes, network)
Streams_paths = Streams_paths_generator(all_paths_matrix, Stream_Source_Destination)
Streams_links_paths = Streams_links_paths_generator(Streams_paths)
Link_order_Descriptor = Link_order_Descriptor_generator(Streams_links_paths, Network_links)
# Preprocessing 
Links_per_Stream = Links_per_Stream_generator(Network_links, Link_order_Descriptor)
Model_Descriptor, Model_Descriptor_vector, Streams = Model_Descriptor_generator(Number_of_Streams, Max_frames, Network_links, Frames_per_Stream, Links_per_Stream)
Frame_Duration = Frame_Duration_Generator(Number_of_Streams, Max_frames, Network_links )
Repetitions, Repetitions_Matrix, Repetitions_Descriptor, max_repetitions= Repetitions_generator(Streams_Period, Streams, Hyperperiod)
unused_links = unused_links_generator(Network_links, Link_order_Descriptor)