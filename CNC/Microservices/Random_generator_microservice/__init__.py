"""

This is an optional microservice designed for simulate the task of the jetconf and topology_discovery microservices.
It generates the same output JSON format queues and send it to the preprocessing microservices.py

You need to manually configure the parameters in the input.conf file :
Number_of_edges, 
Connection_probability,
Number_of_Streams

The code will create the set of necessary parameters and then translate them into json format to send them through the
rabbitmq queues using Pika 
┌───────────────────────────────────┐
│                                   │
│  ┌─────────────────┐              │
│  │ Random_Stream   │              │
│  │    parameters.py│              │  Jet_pre
│  └────────▲────────┘       ┌──────┼───────────┐
│           │                │      │           │
│     ┌─────┴────┐      ┌────┴────┐ │           │
│     │          │      │Rabbitmq │ │    ┌──────▼────────┐
│     │ __init__ ├──────► queues  │ │    │Preprocessing_ │
│     │ .py      │      │   .py   │ │    │Microservice   │
│     └─────┬────┘      └────┬────┘ │    └──────▲────────┘
│           │                │      │           │
│  ┌────────▼────────┐       │      │           │
│  │ RaNet_generat   │       └──────┼───────────┘
│  │ or.py           │              │   top_pre
│  └─────────────────┘              │
│                                   │
└───────────────────────────────────┘
   Random_generator_microservice


"""

from RandStream_Parameters import *
from RanNet_Generator import *
from Rabbitmq_queues import *
import configparser
import json
configParser = configparser.RawConfigParser()   
configFilePath = r'input.conf'
configParser.read(configFilePath)

Number_of_edges = int(configParser.get('random', 'Number_of_edges'))
Connection_probability = float(configParser.get('random', 'Connection_probability'))
Number_of_Streams = int(configParser.get('random', 'Number_of_Streams'))

# topology random geneator

Network_nodes, Network_links, Adjacency_Matrix, plot_network = Random_Network_Generator(Number_of_edges, Connection_probability)
Stream_Source_Destination = Random_flows_generator(Number_of_Streams, Number_of_edges) 

Topology={}
Topology["Network_nodes"]=Network_nodes
Topology["Network_links"]=Network_links 
Topology["Adjacency_Matrix"]=Adjacency_Matrix 

json_Topology = json.dumps(Topology, indent = 4) 
print(json_Topology)

# source destination generator

Stream_information={}

Streams_size , Streams_Period, Streams_Period_list, Deathline_Stream, Number_of_Streams = Random_Stream_size_and_period_generator(Number_of_Streams)
Hyperperiod = Hyperperiod_generator(Streams_Period_list)
Frames_per_Stream, Max_frames, Num_of_Frames = Frames_per_Stream_generator(Streams_size)

Stream_information["Streams_size"] = Streams_size
Stream_information["Streams_Period"]= Streams_Period
Stream_information["Streams_Period_list"]= Streams_Period_list
Stream_information["Deathline_Stream"]= Deathline_Stream
Stream_information["Number_of_Streams"]= Number_of_Streams
Stream_information["Hyperperiod"]= Hyperperiod 
Stream_information["Frames_per_Stream"]=Frames_per_Stream
Stream_information["Max_frames"]=Max_frames
Stream_information["Num_of_Frames"]=Num_of_Frames

json_Stream_information = json.dumps(Stream_information, indent = 4) 

# Sending the messages to the RabbitMQ server
send_message(json_Topology, 'top-pre')
send_message(json_Stream_information, 'jet-pre')