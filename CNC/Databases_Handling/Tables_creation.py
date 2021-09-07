from Cassandra_Connection import Cassandra_connecion

class Tables_creator():
    def  __init__ (self):
        self.tables = {
            "Stream_list" : [
                        "Stream_id text PRIMARY KEY",
                        "talker__stream_rank__rank text",
                        "talker__end_station_interfaces__mac_address text",
                        "talker__end_station_interfaces__interface_name text",
                        "talker__data_frame_specification__index text",
                        "talker__data_frame_specification__field text",
                        "talker__traffic_specification__interval__numerator text",
                        "talker__traffic_specification__interval__denominator text",
                        "talker__traffic_specification__max_frames_per_interval text",
                        "talker__traffic_specification__max_frames_size text",
                        "talker__traffic_specification__transmission_selection text",
                        "talker__traffic_specification__time_aware__earliest_transmit_offset text",
                        "talker__traffic_specification__time_aware__latest_transmit_offset text",
                        "talker__traffic_specification__time_aware__jitter text",
                        "talker__user_to_network_requirements__num_seamless_trees text",
                        "talker__user_to_network_requirements__max_latency text",
                        "talker__interface_capabilities__vlan_tag_capable text",
                        "talker__interface_capabilities__cb_stream_iden_type_list text",
                        "talker__interface_capabilities__cb_sequence_type_list text",
                        "listerner_list__index text",
                        "listerner_list__end_station_interfaces__mac_address text",
                        "listerner_list__end_station_interfaces__interface_name text",
                        "listerner_list__user_to_network_requirements__num_seamless_trees text",
                        "listerner_list__user_to_network_requirements__max_latency text",
                        "listerner_list__interface_capabilities__vlan_tag_capable text",
                        "listerner_list__interface_capabilities__cb_stream_iden_type_list text",
                        "listerner_list__interface_capabilities__cb_sequence_type_list text"
                       ],
            
            "Stream_list_Configuration" : [
                        "Stream_id text PRIMARY KEY",
                        "Status_info__talker_status text",
                        "Status_info__listener_status text",
                        "Status_info__failure_code text",
                        "Failed_interfaces__maccaddress text",
                        "Failed_interfaces__interface_name text",
                        "Talker__accumulated_latency text",
                        "Talker__interface_configuration__interface_list__mac_address text",
                        "Talker__interface_configuration__interface_list__interface_name text",
                        "Talker__interface_configuration__interface_list__config_list__index text",
                        "Talker__interface_configuration__interface_list__config_list__config_value text",
                        "Listener_list__index text",
                        "Listener_list__accumulated_latency text",
                        "Listener_list__interface_configuration__interface_list__mac_address text",
                        "Listener_list__interface_configuration__interface_list__interface_name text",
                        "Listener_list__interface_configuration__interface_list__config_list__index text",
                        "Listener_list__interface_configuration__interface_list__config_list__config_value text"
                        ], 

            "Network_topology" : [
                        "link_index text PRIMARY KEY",
                        "Source_index text",
                        "Source_mac_address text",
                        "Destination_index text",
                        "Destination_mac_address text",
                        "Total_bandwidth text",
                        "Used_bandwidth text",
                        "Associated_Streams text"
                        ],

            "TSN_Bridges": [
                        "bridge_id text PRIMARY KEY",
                        "Mac_adress text",
                        "Capabilities text",
                        "Management_ip_address text"
                        ]
                        }
        self.cassandra = Cassandra_connecion() 
        for table_key in self.tables.keys() :
            print(table_key)
            print(self.tables[table_key])
            self.cassandra.table_creator(table_key,self.tables[table_key])

tables = Tables_creator()