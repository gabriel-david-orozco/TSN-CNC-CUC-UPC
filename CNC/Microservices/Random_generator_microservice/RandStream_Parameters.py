## This set of functions is for the random statement of the parameters of the network
import random
from math import gcd

from RanNet_Generator import Random_Network_Generator

"""
Fortunately the only input is the number of streams in the network
# Number of streams

"""


########## PARAMETERS ##########
# Stream_size (Provided - Randomized)
# Streams_Period (Provided - Randomized)
# Streams_Period_list (generated)
# Hiperperiod (generated)
# Frames_per_Stream (generated) 
# Max_frames, (generated)
# Num_of_Frames (generated)
# Deathline_Stream (Provided - Randomized)

def Random_Stream_size_and_period_generator(Number_of_Streams): 
    # In the Luxembourg paper the proportions of the code is as follows:
    #15% Audio streams 
        #• 128 or 256 byte frames • periods: one frame each 1.25ms • deadline constraints either 5 or 10ms
    #16% Video Streams
        # 
    #69% Control Streams
    # Stream sizes are in bytes
    # Stream periods are in nano seconds
    type_selector = random.choices([1,2,3],weights=(16,15,69), k= Number_of_Streams)
    print("THis is the type selector", type_selector)
    Streams_size = []
    Streams_Period = {}
    Streams_Period_list = [(v[0]) for k, v in Streams_Period.items()]
    Deathline_Stream = {}
    for i in range(len(type_selector)) :
        if type_selector[i] == 1: # Audio
            Streams_size.append(256)
            Streams_Period[(i)] = 2500
            Deathline_Stream[(i)] = 10000
        if type_selector[i] == 2: # Video
            Streams_size.append(30 * 1500)
            Streams_Period[(i)] = 30000
            Deathline_Stream[(i)] = 10000
        if type_selector[i] == 3: # Control
            Streams_size.append(53)
            Streams_Period[(i)] = 5000
            Deathline_Stream[(i)] = 5000
    Streams_Period_list = [v for k,v in Streams_Period.items()]
    
    #for i in range(len(Streams_Period)):
    #    Streams_Period[(i)] = Streams_Period[(i)][0]
    return Streams_size , Streams_Period, Streams_Period_list, Deathline_Stream, Number_of_Streams

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
        print(repetition, type(repetition))
        Frames_per_Stream.append([1 for frame in range(int(float(repetition)/1500))])
        Frames_per_Stream = [x if x else [1] for x in Frames_per_Stream]

    Max_frames = max([len(frame) for frame in Frames_per_Stream])
    Num_of_Frames = []
    for i in Frames_per_Stream : Num_of_Frames.append(len(i))
    return Frames_per_Stream, Max_frames, Num_of_Frames
