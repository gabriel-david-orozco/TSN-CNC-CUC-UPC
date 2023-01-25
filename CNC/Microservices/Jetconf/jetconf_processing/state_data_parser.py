import json
from math import gcd
from Rabbitmq_queues import *

def Hyperperiod_generator(Streams_Period_list) :
    Hyperperiod = 1
    for i in Streams_Period_list:
        Hyperperiod = Hyperperiod*i//gcd(Hyperperiod, i)
    return Hyperperiod
 
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


# Opening JSON file
with open('state_data.json') as json_file:
    data = json.load(json_file)

streams_id_list = [stream_id["stream-id"] for stream_id in data["ieee802-dot1q-tsn-types-upc-version:tsn-uni"]["stream-list"]]
# getting stream size

Streams_size = [stream_id["request"]["talker"]["traffic-specification"]["max-frame-size"] for stream_id in data["ieee802-dot1q-tsn-types-upc-version:tsn-uni"]["stream-list"]]

# Number of streams

Number_of_Streams = len(Streams_size)

# frames per stream
Frames_per_stream = [[stream_id["request"]["talker"]["traffic-specification"]["max-frames-per-interval"] for stream_id in data["ieee802-dot1q-tsn-types-upc-version:tsn-uni"]["stream-list"]]]
max_frames = max(Frames_per_stream,)

# Deathline_Stream

Deathline_Stream_list = [stream_id["request"]["talker"]["user-to-network-requirements"]["max-latency"] for stream_id in data["ieee802-dot1q-tsn-types-upc-version:tsn-uni"]["stream-list"]]

Deathline_Stream_int = {}
for i in range(len(Deathline_Stream_list)) :
    Deathline_Stream_int[i] = Deathline_Stream_list[i]

Deathline_Stream = { str(key) : value for key, value in Deathline_Stream_int.items() }

# Frames per stream
Frames_per_stream = [stream_id["request"]["talker"]["traffic-specification"]["max-frames-per-interval"] for stream_id in data["ieee802-dot1q-tsn-types-upc-version:tsn-uni"]["stream-list"]]
max_frames = max(Frames_per_stream)

# Intervals
interval_denominator = [stream_id["request"]["talker"]["traffic-specification"]["interval"]["denominator"] for stream_id in data["ieee802-dot1q-tsn-types-upc-version:tsn-uni"]["stream-list"]]
interval_numerator = [stream_id["request"]["talker"]["traffic-specification"]["interval"]["numerator"] for stream_id in data["ieee802-dot1q-tsn-types-upc-version:tsn-uni"]["stream-list"]]

#getting the Frames_per_stream

per_stream_period= {}
Streams_Period_list = []
for i in range(len(interval_denominator)) :
    Streams_Period_list.append(int(interval_numerator[i]/interval_denominator[i]))
    per_stream_period[i] = int(interval_numerator[i]/interval_denominator[i]) # this goes in nanoseconds
Streams_Period = { str(key) : value for key, value in per_stream_period.items() }

# Generating the hyperperiod
Hyperperiod = Hyperperiod_generator(Streams_Period_list)

# Generating Frames_per_Stream, Max_frames, Num_of_Frames
Frames_per_Stream, Max_frames, Num_of_Frames = Frames_per_Stream_generator(Streams_size)

# Defining the json_payload 

jetconf_payload = {}

jetconf_payload["Streams_size"] = Streams_size
jetconf_payload["Streams_Period"] = Streams_Period
jetconf_payload["Streams_Period_list"] = Streams_Period_list
jetconf_payload["Deathline_Stream"] = Deathline_Stream
jetconf_payload["Number_of_Streams"] = Number_of_Streams
jetconf_payload["Hyperperiod"] = Hyperperiod
jetconf_payload["Frames_per_Stream"] = Frames_per_Stream
jetconf_payload["Max_frames"] = Max_frames
jetconf_payload["Num_of_Frames"] = Num_of_Frames

print("############# This is the json payload #############")

print(jetconf_payload)

json_jetconf_payload = json.dumps(jetconf_payload, indent = 4) 
send_message(json_jetconf_payload, 'jet-pre')
