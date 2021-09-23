## This set of functions is for the random statement of the parameters of the network
import random
from math import gcd

from RanNet_Generator import Random_Network_Generator
from Path_Calculator import *

def Random_Stream_size_and_period_generator(Links_per_Stream): 
    Posible_Streams_Sizes = [1500, 3000, 4500, 6000]
    Posible_Streams_Periods = [200, 400, 800]
    Streams_size = []
    Streams_Period = {}
    for stream_index in range(len(Links_per_Stream)) :
        Streams_size.append(random.sample(Posible_Streams_Sizes, 1)) # This is the size of the packages in bytes
        Streams_Period[(stream_index)] = random.sample(Posible_Streams_Periods, 1) # This is the period in micro seconds
    
    print("#######################Streams_size and Stream Period#################")    
    print(Streams_size)
    print(Streams_Period)
    Streams_Period_list = [(v[0]) for k, v in Streams_Period.items()]
    
    for i in range(len(Streams_Period)):
        Streams_Period[(i)] = Streams_Period[(i)][0]
    return Streams_size , Streams_Period, Streams_Period_list

# This funciton reads the periods of the strems and provides the hyperperiod (lcm of all the periods)
def Hyperperiod_generator(Streams_Period_list) :
    Hyperperiod = 1
    for i in Streams_Period_list:
        Hyperperiod = Hyperperiod*i//gcd(Hyperperiod, i)
    return Hyperperiod

# This function generates the frames_per_stream, basically a list with the number of frames per stream represented 
# as a set of 1's
# Provides also the maximum number of frames in an stream
def Frames_per_Stream_generator(Streams_size):
    Frames_per_Stream = []
    for repetition in (Streams_size):
        print(repetition[0], type(repetition[0]))
        Frames_per_Stream.append([1 for frame in range(int(float(repetition[0])/1500))])
    
    Max_frames = max([len(frame) for frame in Frames_per_Stream])
    Num_of_Frames = []
    for i in Frames_per_Stream : Num_of_Frames.append(len(i))
    return Frames_per_Stream, Max_frames, Num_of_Frames


# Stream_Source_Destination = Random_flows_generator(Number_of_Streams, Number_of_edges)
# network = Network_Topology(Adjacency_Matrix) # Using the Network Topology class
# all_paths_matrix = all_paths_matrix_generator(Network_nodes, network)
# Streams_paths = Streams_paths_generator(all_paths_matrix, Stream_Source_Destination)
# Streams_links_paths = Streams_links_paths_generator(Streams_paths)
# Link_order_Descriptor = Link_order_Descripto_generator(Streams_links_paths)
# Links_per_Stream = Links_per_Stream_generator(Network_links, Link_order_Descriptor)
# Streams_size , Streams_Period, Streams_Period_list = Random_Stream_size_and_period_generator(Links_per_Stream)
# Hyperperiod = Hyperperiod_generator(Streams_Period_list)
# Frames_per_Stream, Max_frames, Num_of_Frames = Frames_per_Stream_generator(Streams_size)
