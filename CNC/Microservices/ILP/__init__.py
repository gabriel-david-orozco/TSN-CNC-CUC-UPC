from ILP_Generator import *
from time import time
scheduler = ILP_Raagard_solver(Number_of_Streams, Network_links, \
                Link_order_Descriptor, \
                Streams_Period, Hyperperiod, Frames_per_Stream, Max_frames, Num_of_Frames, \
                Model_Descriptor, Model_Descriptor_vector, Deathline_Stream, \
                Repetitions, Repetitions_Descriptor, unused_links, Frame_Duration)
instance, results = scheduler.instance, scheduler.results
final_time = time.time()
