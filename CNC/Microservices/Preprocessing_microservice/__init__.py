import pika

from Djikstra_Path_Calculator import *
from Preprocessing import *

"""
This code should receive as input:

-------------- For the djikstra --------------
Topology["Adjacency_Matrix"] (rand_net)
Topology["Network_nodes"] (rand_net)
Stream_Source_Destination (rand_net) This value has to be regard as it is not properly from the rand net
Topology["Network_links"] (rand_net)

-------------- For the preprocessing --------------

Topology["Network_links"] (rand network)
Link_order_Descriptor (djikstra)
Number_of_streams (rand stream parameters)
max_frames (rand stream parameters)
Topology["Network_links"] (rand network)
Stream_information["Frames_per_Stream"] (ran stream parameters)
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
import json
from Rabbitmq_queues import *

if __name__ == "__main__":
    
   
   topo_flag = os.path.exists('/var/topology.txt')
   jetconf_flag = os.path.exists  ('/var/jetconf.txt')
   if(topo_flag and jetconf_flag):
      with open('/var/topology.txt') as topology_json_file:
         Topology = json.load(topology_json_file)
      with open('/var/jetconf.txt') as jetconf_json_file:
         Stream_information = json.load(jetconf_json_file)   
      # Djikstra scheduler

      network = Network_Topology(Topology["Adjacency_Matrix"]) # Using the Network Topology class
      all_paths_matrix = all_paths_matrix_generator(Topology["Network_nodes"], network)
      Streams_paths = Streams_paths_generator(all_paths_matrix, Topology["Stream_Source_Destination"])
      Streams_links_paths = Streams_links_paths_generator(Streams_paths)
      Link_order_Descriptor = Link_order_Descriptor_generator(Streams_links_paths, Topology["Network_links"])

      # Preprocessing
      Links_per_Stream = Links_per_Stream_generator(Topology["Network_links"], Link_order_Descriptor)
      Model_Descriptor, Model_Descriptor_vector, Streams = Model_Descriptor_generator(Stream_information["Number_of_Streams"], Stream_information["Max_frames"], Topology["Network_links"], Stream_information["Frames_per_Stream"], Links_per_Stream)
      Frame_Duration = Frame_Duration_Generator(Stream_information["Number_of_Streams"], Stream_information["Max_frames"], Topology["Network_links"] )
      Repetitions, Repetitions_Matrix, Repetitions_Descriptor, max_repetitions= Repetitions_generator(Stream_information["Streams_Period"], Streams, Stream_information["Hyperperiod"])
      unused_links = unused_links_generator(Topology["Network_links"], Link_order_Descriptor)

      Preprocessed_data = {}

      Preprocessed_data["Number_of_Streams"] = Stream_information["Number_of_Streams"]
      Preprocessed_data["Stream_Source_Destination"] = Topology["Stream_Source_Destination"]
      Preprocessed_data["identificator"] = Topology["identificator"]
      Preprocessed_data["interface_Matrix"] = Topology["interface_Matrix"]
      Preprocessed_data["Network_links"] = Topology["Network_links"]
      Preprocessed_data["Adjacency_Matrix"] = Topology["Adjacency_Matrix"]
      Preprocessed_data["Link_order_Descriptor"] = Link_order_Descriptor
      Preprocessed_data["Streams_Period"] = Stream_information["Streams_Period"]
      Preprocessed_data["Hyperperiod"] = Stream_information["Hyperperiod"]
      Preprocessed_data["Frames_per_Stream"] = Stream_information["Frames_per_Stream"]
      Preprocessed_data["Max_frames" ] = Stream_information["Max_frames"]
      Preprocessed_data["Streams_size"] = Stream_information["Streams_size"]
      Preprocessed_data["Num_of_Frames"] = Stream_information["Num_of_Frames"]
      Preprocessed_data["Model_Descriptor"] = Model_Descriptor
      Preprocessed_data["Model_Descriptor_vector"] = Model_Descriptor_vector
      Preprocessed_data["Deathline_Stream"] = Stream_information["Deathline_Stream"]
      Preprocessed_data["Repetitions"] = Repetitions
      Preprocessed_data["Repetitions_Descriptor"] = Repetitions_Descriptor
      Preprocessed_data["Frame_Duration"] = Frame_Duration
      Preprocessed_data["unused_links"] =unused_links
      Preprocessed_data["Links_per_Stream"] = Links_per_Stream

      print(Preprocessed_data)
      json_Preprocessed_data = json.dumps(Preprocessed_data, indent = 4) 
      print("working")
      # Sending the messages to the RabbitMQ server
      send_message(json_Preprocessed_data, 'pre-ilp')
   else:
      print("There is not input data, check the previous microservices or the RabbitMQ logs")
