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
          Preprocessed_data = json.load(preprocessing_json_file)
       print(Preprocessed_data['Deathline_Stream'])
       print("______________")
       print(Preprocessed_data['Streams_Period'])
       Deathline_Stream= {int(k):v for k,v in Preprocessed_data['Deathline_Stream'].items()}
       Streams_Period= {int(k):v for k,v in Preprocessed_data['Streams_Period'].items()}
       Model_Descriptor=restructuring_dictionary(Preprocessed_data['Model_Descriptor'])
       Frame_Duration=restructuring_dictionary(Preprocessed_data['Frame_Duration'])
       Model_Descriptor_vector= Preprocessed_data['Model_Descriptor_vector']
       Num_of_Frames=Preprocessed_data['Num_of_Frames']
       Link_order_Descriptor=Preprocessed_data['Link_order_Descriptor']
       Network_links=Preprocessed_data['Network_links']
       Adjacency_Matrix = Preprocessed_data['Adjacency_Matrix']
       Stream_Source_Destination=Preprocessed_data['Stream_Source_Destination']
       Links_per_Stream=Preprocessed_data['Links_per_Stream']
       Frames_per_Stream=Preprocessed_data['Frames_per_Stream']
       Streams_size=Preprocessed_data['Streams_size']

       scheduler = ILP_Raagard_solver(Preprocessed_data['Number_of_Streams'], Preprocessed_data['Network_links'], \
                        Preprocessed_data['Link_order_Descriptor'], \
                        Streams_Period, Preprocessed_data['Hyperperiod'], Preprocessed_data['Frames_per_Stream'], \
                        Preprocessed_data['Max_frames'], Preprocessed_data['Num_of_Frames'], \
                        Model_Descriptor, Preprocessed_data['Model_Descriptor_vector'], Deathline_Stream, \
                        Preprocessed_data['Repetitions'], Preprocessed_data['Repetitions_Descriptor'], Preprocessed_data['unused_links'], Frame_Duration)
       instance, results = scheduler.instance, scheduler.results
       Feasibility_indicator, Result_offsets, Clean_offsets_collector, Results_latencies  = ILP_results_visualizer(instance, Model_Descriptor_vector)
       print('This is the feasibility you are looking for', Feasibility_indicator)
       dataframe_printer(instance, Clean_offsets_collector, Results_latencies, Feasibility_indicator, Adjacency_Matrix, Stream_Source_Destination,
                Link_order_Descriptor, Links_per_Stream, Frames_per_Stream, Deathline_Stream, Streams_Period, Streams_size)





    else:
        print("There is not input data, check the previous microserrvices or the RabbitMQ logs")
