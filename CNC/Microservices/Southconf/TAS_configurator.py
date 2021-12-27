'''
This function generates a dictionary that organizes the data of the offets.
The json load of the restconf configuration values provided are:
admin-control-list-lenght
time-interval-value
'''

import copy
def gates_parameter_generator(Clean_offsets):
    grouped_offsets = {}
    for frame in Clean_offsets:
        identificator=frame['Task'].split(',')
        try:
            grouped_offsets[identificator[3]][identificator[1]].append(frame['Start'])
        except:
            try:
                grouped_offsets[identificator[3]][identificator[1]] = [frame['Start']]
            except :
                grouped_offsets[identificator[3]]= {identificator[1] : [frame['Start']]}

    return grouped_offsets
       
'''This function generates the period to be used as admin cycle time'''
def full_scheduler_generator(grouped_offsets, Repetitions_Descriptor, Streams_Period):
    stream_index = 0
    for repetitions in Repetitions_Descriptor:
        for repetition in repetitions:

            for link in grouped_offsets.keys():
                if " " + str(stream_index) in grouped_offsets[link].keys():
                    if repetition != 0:
                        repetition_offsets = [x+ Streams_Period[str(stream_index)]*repetition for x in grouped_offsets[link][" " + str(stream_index)]]
                        print("looking for this shit", grouped_offsets[link][" " + str(stream_index)])
                        print("and its type", type(grouped_offsets[link][" " + str(stream_index)]))
                        print(f"link index {link}  stream_index  {stream_index}")
                        for new_offset in repetition_offsets:
                            grouped_offsets[link][" " + str(stream_index)].append(new_offset)
        stream_index += 1
    return grouped_offsets


''' 
The following fucntion presents the values in the following way (example):
gate-state-values= [128, "in binary 10000000
                    128, "in binary 10000000
                    255], "in binary 11111111
time-interval-values=[1000
                    2000
                    3000]

With this values is enough to build the admin-control-list of the json payload
'''
def gates_states_values_generator(grouped_offsets, priority_mapping):
    # organize the offsets per link and time
    gates_states={}
    for link in grouped_offsets.keys():
        offsets_organizer= {}
        for stream in grouped_offsets[link].keys():
            for repetition in grouped_offsets[link][stream]:
                offsets_organizer[repetition] = stream
        offsets_organizer= {x:offsets_organizer[x] for x in sorted(offsets_organizer)}
        gates_states[link] = offsets_organizer
    
    #Change stream identificator for priority in binary
    new_gates_states = copy.deepcopy(gates_states)
    for link in gates_states.keys():
        for gate in gates_states[link].keys():
            for i in range(7):
                if gates_states[link][gate] == " "+str(i) :
                    print("link and gate", link, gate)
                    new_gates_states[link][gate] = 2**i
    
    #This will add the best effort traffics
    new_gates_states_be = copy.deepcopy(new_gates_states)
    for key, link in new_gates_states.items():
        for time_interval in link.keys():
            new_gates_states_be[key][time_interval+12] = 255 # This has a hardcoded 12 because it is the duration of the link
    
    # Final_sort
    final_sorted_offsets= {} 
    for link in new_gates_states_be.keys():
        final_sorted_offsets[link] = {x: new_gates_states_be[link][x] for x in sorted(new_gates_states_be[link])}
    return final_sorted_offsets
    
hyperperiod= 5000
Repetitions_Descriptor = [[0, 0], [0, 1], [0, 1], [0, 1], [0, 1]]
Clean_offsets = [{'Task': "('S', 0, 'L', 6, 'F', 0)", 'Start': 1.0}, 
                {'Task': "('S', 1, 'L', 0, 'F', 0)", 'Start': 124.0}, 
                {'Task': "('S', 1, 'L', 4, 'F', 0)", 'Start': 1.0}, 
                {'Task': "('S', 2, 'L', 4, 'F', 0)", 'Start': 2377.0}, 
                {'Task': "('S', 3, 'L', 1, 'F', 0)", 'Start': 1.0}, 
                {'Task': "('S', 4, 'L', 0, 'F', 0)", 'Start': 1.0}]
Streams_Period=  {'0': 5000, '1': 2500, '2': 2500, '3': 2500, '4': 2500}
# The priority number 7 is always for ptp traffic
priority_mapping= {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '7'} 
grouped_offsets=gates_parameter_generator(Clean_offsets)
print(grouped_offsets[" 6"][" 0"])

grouped_offsets=full_scheduler_generator(grouped_offsets, Repetitions_Descriptor, Streams_Period)
print(grouped_offsets)

gates_states = gates_states_values_generator(grouped_offsets, priority_mapping)
print("_______________ Looking for the gate states _______________")
print(gates_states)
print(gates_states[' 6'])
print(type(gates_states[' 6']))