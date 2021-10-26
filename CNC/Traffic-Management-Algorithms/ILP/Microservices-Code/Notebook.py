import random

from numpy import empty
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
    print("This is the type selector", type_selector)
    Streams_size = []
    Streams_Period = {}
    for i in range(len(type_selector)) :
        if type_selector[i] == 1: # Audio
            Streams_size.append(256)
            Streams_Period[(i)] = 1250
        if type_selector[i] == 2: # Video
            Streams_size.append(3000)
            Streams_Period[(i)] = 30000
        if type_selector[i] == 3: # Control
            Streams_size.append(53)
            Streams_Period[(i)] = 5000
    Streams_Period_list = [v for k,v in Streams_Period.items()]
    
    #for i in range(len(Streams_Period)):
    #    Streams_Period[(i)] = Streams_Period[(i)][0]
    return Streams_size , Streams_Period, Streams_Period_list


def Frames_per_Stream_generator(Streams_size):
    Frames_per_Stream = []
    for repetition in (Streams_size):
        Frames_per_Stream.append([1 for frame in range(int(float(repetition)/1500))])
        Frames_per_Stream = [x if x else [1] for x in Frames_per_Stream]

    Max_frames = max([len(frame) for frame in Frames_per_Stream])
    Num_of_Frames = []
    for i in Frames_per_Stream : Num_of_Frames.append(len(i))
    return Frames_per_Stream, Max_frames, Num_of_Frames

Streams_size , Streams_Period, Streams_Period_list = Random_Stream_size_and_period_generator(5)
print("######## Stream Size")
print(Streams_size)
print("######## Streams period")
print(Streams_Period)
print("######## Streams period list")
print(Streams_Period_list)

Frames_per_Stream, Max_frames, Num_of_Frames = Frames_per_Stream_generator(Streams_size)

print("######## Frames per stream")
print(Frames_per_Stream)