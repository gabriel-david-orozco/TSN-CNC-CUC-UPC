from ILP_Generator import *
from Solutions_Visualizer import *
from time import time
import os
import json

'''
this is the list of input elements:


'Number_of_Streams',
'Network_links', 
'Link_order_Descriptor', 
'Streams_Period', 
'Hyperperiod', 
'Frames_per_Stream', 
'Max_frames', 
'Num_of_Frames', 
'Model_Descriptor', 
'Model_Descriptor_vector', 
'Deathline_Stream', 
'Repetitions', 
'Repetitions_Descriptor', 
'Frame_Duration', 
'unused_links'
'''
def restructuring_dictionary(dictionary):
    correct_keys=[]
    for key in dictionary.keys():
        new_key = tuple(key.split("_"))
        new_key= [int(x) for x in new_key]
        new_key=tuple(new_key) 
        correct_keys.append(new_key)
        new_values= dictionary.values()
    zip_iterator = zip(correct_keys, new_values)
    final_dictionary = dict(zip_iterator)
    return final_dictionary

if __name__ == "__main__":

    preprocessing_flag = os.path.exists('/var/preprocessing.txt')
    if(preprocessing_flag):
       with open('/var/preprocessing.txt') as preprocessing_json_file:
          preprocessing = json.load(preprocessing_json_file)
       print(preprocessing['Deathline_Stream'])
       print("______________")
       print(preprocessing['Streams_Period'])
       Deathline_Stream= {int(k):v for k,v in preprocessing['Deathline_Stream'].items()}
       Streams_Period= {int(k):v for k,v in preprocessing['Streams_Period'].items()}
       Model_Descriptor=restructuring_dictionary(preprocessing['Model_Descriptor'])
       Frame_Duration=restructuring_dictionary(preprocessing['Frame_Duration'])
       Model_Descriptor_vector= preprocessing['Model_Descriptor_vector']
       Num_of_Frames=preprocessing['Num_of_Frames']
       Link_order_Descriptor=preprocessing['Link_order_Descriptor']
       Network_links=preprocessing['Network_links']

       scheduler = ILP_Raagard_solver(preprocessing['Number_of_Streams'], preprocessing['Network_links'], \
                        preprocessing['Link_order_Descriptor'], \
                        Streams_Period, preprocessing['Hyperperiod'], preprocessing['Frames_per_Stream'], \
                        preprocessing['Max_frames'], preprocessing['Num_of_Frames'], \
                        Model_Descriptor, preprocessing['Model_Descriptor_vector'], Deathline_Stream, \
                        preprocessing['Repetitions'], preprocessing['Repetitions_Descriptor'], preprocessing['unused_links'], Frame_Duration)
       instance, results = scheduler.instance, scheduler.results
       Feasibility_indicator, Result_offsets, Clean_offsets_collector, Results_latencies  = ILP_results_visualizer(instance, Model_Descriptor_vector)
       print('This is the feasibility you are looking for', Feasibility_indicator)
       #dataframe_printer(instance, Clean_offsets_collector, Results_latencies, Feasibility_indicator, Adjacency_Matrix, Stream_Source_Destination,
       #         Link_order_Descriptor, Links_per_Stream, Frames_per_Stream, Deathline_Stream, Streams_Period, Streams_size)





    else:
        print("There is not input data, check the previous microserrvices or the RabbitMQ logs")
