## This set of functions is for the random statement of the parameters of the network
import random
from math import gcd

Posible_Streams_Sizes = [1500, 3000, 4500, 6000]
Posible_Streams_Periods = [200, 400, 800]

def Random_Stream_size_and_period_generator(Links_per_Stream, Posible_Streams_Sizes, Posible_Streams_Periods): 
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
    print("the same streams_periods but after the funny loop",Streams_Period)
    return Streams_size , Streams_Period, Streams_Period_list

def Hyperperiod_generator(Streams_Period_list) :
    Hyperperiod = 1
    for i in Streams_Period_list:
        Hyperperiod = Hyperperiod*i//gcd(Hyperperiod, i)
    return Hyperperiod




Streams_size , Streams_Period, Streams_Period_list = Random_Stream_size_and_period_generator(Links_per_Stream)
Hyperperiod = Hyperperiod_generator(Streams_Period_list)