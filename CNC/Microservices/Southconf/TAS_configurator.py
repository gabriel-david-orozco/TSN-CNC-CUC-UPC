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
        stream_index = stream_index +  1
    return grouped_offsets


''' 
The following fucntion presents the values in the following way (example):
gate-states-values= [128, "in binary 10000000
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


'''
Generates the payload defined in the 802.1 qcc schedule
'''
def payload_generator(Clean_offsets, Repetitions_Descriptor, Streams_Period,priority_mapping, hyperperiod):

    grouped_offsets=gates_parameter_generator(Clean_offsets)
    grouped_offsets=full_scheduler_generator(grouped_offsets, Repetitions_Descriptor, Streams_Period)
    final_sorted_offsets = gates_states_values_generator(grouped_offsets, priority_mapping)

    per_link_payload = {}
    for link, streams in final_sorted_offsets.items():
        
        admin_control_list = []
        offsets_list = list(streams.keys())
        print("Looking for the offsets_list don't you?", offsets_list)
        offsets_index= 0
        to_define = "PORT_0"
        for gate_state in streams.values():
            # Evaluate a offset with the next offset to get the total duration of the transmission
            # Until this moment, all offsets and period values were in microseconds
            try:
                time_interval_value = str(int(1000*(offsets_list[offsets_index +1 ] - offsets_list[offsets_index])))
            except:
                print("______________The mistake you are looking for _______________________")
                print(hyperperiod, " __ ", offsets_list[offsets_index])
                time_interval_value = str(int(1000*(hyperperiod - offsets_list[offsets_index]) + 1000))
            sgs_params = {"gate-states-value": str(int(gate_state)),

                          "time-interval-value" :time_interval_value # Nanoseconds
                        }
            admin_control_list.append(
                {
                    "index": str(offsets_index),
                    "operation-name": "set-gate-states",
                    "sgs-params": sgs_params
                }
            )
            offsets_index = offsets_index + 1
        per_link_payload[link] = {
            "interface": 
            {
                "name": to_define,
                "type" : "iana-if-type:ethernetCsmacd",
                "ieee802-dot1q-sched:gate-parameters": {
                    "admin-gate-states": "255",
                    "gate-enabled": "true",
                    "admin-control-list-length": len(offsets_list),
                    "config-change": "true",
                    "admin-cycle-time": {
                        "numerator": "1",
                        "denominator": str(int(1000000/(hyperperiod)))
                    },
                    "admin-control-list" : admin_control_list,
                    "admin-base-time": {
                        "seconds": "0",
                        "fractional-seconds": "0"
                    },
                    "admin-cycle-time-extension": "0"
                }
            }
        } 
    return per_link_payload

# hyperperiod= 32_000 # Hyperperiod is in microseconds
# Repetitions_Descriptor = [[0, 0], [0, 1], [0, 1], [0, 1], [0, 1]]
# Clean_offsets = [{'Task': "('S', 0, 'L', 6, 'F', 0)", 'Start': 1.0}, 
#                 {'Task': "('S', 1, 'L', 0, 'F', 0)", 'Start': 124.0}, 
#                 {'Task': "('S', 1, 'L', 4, 'F', 0)", 'Start': 1.0}, 
#                 {'Task': "('S', 2, 'L', 4, 'F', 0)", 'Start': 2377.0}, 
#                 {'Task': "('S', 3, 'L', 1, 'F', 0)", 'Start': 1.0}, 
#                 {'Task': "('S', 4, 'L', 0, 'F', 0)", 'Start': 1.0}]
# Streams_Period=  {'0': 32_000, '1': 32_000, '2': 32_000, '3': 16_000, '4': 32_000} # streams_periods are in microseconds 

# # The chu
# # The priority number 7 is always for ptp traffic
# priority_mapping= {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '7'} 
# per_link_payload = payload_generator(Clean_offsets, Repetitions_Descriptor, Streams_Period,priority_mapping, hyperperiod)
# print(per_link_payload)