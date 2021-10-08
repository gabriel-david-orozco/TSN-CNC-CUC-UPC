# This is the list of elements that should be provided as input parameters:

# Stream source and destination
# Path per Stream
# Deathline of each stream
# Period of each stream
# Size of the Stream 
# Maximum Sinchronization error

# This code generates a random network of n nodes and m links

from networkx.generators.random_graphs import erdos_renyi_graph

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from math import gcd

# This function generates the adjacency Matrix
def adj(connections):
    ##step 1
    temp=(set(elem[0] for elem in connections).union(
        set(elem[1] for elem in connections)))
    n=max(temp)+1
    ans=[]
    ##step 2
    for i,_ in enumerate(temp):
        ans.append([])
        for j,_ in enumerate(temp):
            ans[i].append(0)
    ##step 3
    for pair in connections:
        ans[pair[0]][pair[1]]=1
        ans[pair[1]][pair[0]]=1
    return ans

Number_of_edges = 2 # Number of edges
Connection_probability = 0.9 # Probability of connection

# Determine if a list has a 0 element
def allcmp(existing_indicator) :
    for item in existing_indicator :
        if item == 0 :
            return False
    return True

# Validates if all the elements in the matrix are connected
def Matrix_Validator(element_list):
    existing_indicator = [0 for i in range(len(element_list[0]))]
    x = 0
    for element in element_list :
        y = 0 
        for element_2 in element :
            existing_indicator[y] = existing_indicator[y] + element_2
            y = y +1
        x = x +1
    return allcmp(existing_indicator)

# This function generates the Random Network 

def Random_Network_Generator(Number_of_edges, Connection_probability) :
    ensurer = False
    while ensurer == False :
        g = erdos_renyi_graph(Number_of_edges, Connection_probability)

        Network_nodes =  list(g.nodes)
        Network_links = list(g.edges)
        Sources = [link[0] for link in Network_links]
        Destinations = [link[1] for link in Network_links]

        # Checks if the random values are suitable for the Adjacency Matrix
        try: 
            Adjacency_Matrix = adj(Network_links)
            ensurer = Matrix_Validator(Adjacency_Matrix) # Determine if the all the nodes are connected
            if len(Adjacency_Matrix) != Number_of_edges:
                ensurer = False
        except:
            ensurer = False 
            

    # Build a dataframe with the Source and destination connections

    df = pd.DataFrame({ 'from': Sources , 'to': Destinations})

    # Build the graph
    G=nx.from_pandas_edgelist(df, 'from', 'to')

    # Plot the graph
    plot_network = plt.figure(1, figsize=(14, 7))
    plt.subplot(221)
    plt.title("Network Topology")
    nx.draw(G, with_labels=True)

    return Network_nodes, Network_links, Adjacency_Matrix, plot_network
Network_nodes, Network_links, Adjacency_Matrix, plot_network = Random_Network_Generator(Number_of_edges, Connection_probability)

####################################################################################
################### FROM THIS PART THE DJIKSTRA ALGORITH STARTS ####################
####################################################################################


Number_of_Streams = 5

# This function generates a set of flows from a destination to an end
def Random_flows_generator(Number_of_Streams, Number_of_edges) :
    Stream_Source_Destination = []
    for i in range(Number_of_Streams) :
        Stream_Source_Destination.append(random.sample(range(0, Number_of_edges), 2))
    return Stream_Source_Destination

Stream_Source_Destination = Random_flows_generator(Number_of_Streams, Number_of_edges)

# Djikstra algorithm is here !
class Network_Topology(): 
    # A constructor to iniltialize the values
    def __init__(self, graph):
        nodes = len(graph)
        #distance array initialization
        self.distArray = [0 for i in range(nodes)]
        #visited nodes initialization
        self.vistSet = [0 for i in range(nodes)]
        #initializing the number of nodes
        self.V = nodes
        #initializing the infinity value
        self.INF = 1000000
        #initializing the graph matrix
        #self.graph = [[0 for column in range(nodes)]  
        #            for row in range(nodes)]
        self.graph = graph    
    def dijkstra(self, srcNode):
        for i in range(self.V):
          #initialise the distances to infinity first
          self.distArray[i] = self.INF
          #set the visited nodes set to false for each node
          self.vistSet[i] = False
        #initialise the first distance to 0
        self.distArray[srcNode] = 0
        paths={}
        for i in range(self.V): 
  
            # Pick the minimum distance node from  
            # the set of nodes not yet processed.  
            # u is always equal to srcNode in first iteration 
            u = self.minDistance(self.distArray, self.vistSet) 
  
            # Put the minimum distance node in the  
            # visited nodes set
            self.vistSet[u] = True
             # Update dist[v] only if is not in vistSet, there is an edge from 
            # u to v, and total weight of path from src to  v through u is 
            # smaller than current value of dist[v]
            for v in range(self.V): 
                if self.graph[u][v] > 0 and self.vistSet[v] == False and self.distArray[v] > self.distArray[u] + self.graph[u][v]: 
                        self.distArray[v] = self.distArray[u] + self.graph[u][v]
                        # This is for creating a dictorionary that stores the keys and values of the node and the last visited node in the path
                        # Used for generating the list with the elements on the paths
                        paths[v] = u 
        self.full_paths_set = []
        for i in range(0,self.V):
            full_path =  self.paths_generator(i, srcNode , paths, [])
            self.full_paths_set.append(full_path)
        
        self.printSolution(self.distArray)

    #A utility function to find the node with minimum distance value, from 
    # the set of nodes not yet included in shortest path tree 
    def minDistance(self, distArray, vistSet): 
  
        # Initilaize minimum distance for next node
        min = self.INF
  
        # Search not nearest node not in the  
        # unvisited nodes
        for v in range(self.V): 
            if distArray[v] < min and vistSet[v] == False: 
                min = distArray[v] 
                min_index = v 
  
        return min_index

    def printSolution(self, distArray): 
        print ("Node \tDistance from 0")
        for i in range(self.V): 
            print (i, "\t", distArray[i])

    #This recursive function generates the path from a source to a destination based on the paths
    def paths_generator(self, node, source, paths, full_path_per_node):
        if node != source:
            if paths[node] != source:
                full_path_per_node.append(paths[node])
                self.paths_generator(paths[node], source, paths, full_path_per_node)
            else:
                return [source]
        else :
            full_path_per_node = []
        return full_path_per_node

# Using the Network Topology class
network = Network_Topology(Adjacency_Matrix) 

# This is function generates a matrix with all the paths from one node to the other calculated by djikstra
def all_paths_matrix_generator(Network_nodes, network) :
    all_paths_matrix = [] 
    for node in Network_nodes:
        network.dijkstra(node) # This matrix saves all the existing paths in the network from one point to the othe 
        all_paths_matrix.append(network.full_paths_set)
    return all_paths_matrix
all_paths_matrix = all_paths_matrix_generator(Network_nodes, network)


# Determining the path for each Stream generating a list of of all the nodes from source to destination
def Streams_paths_generator(all_paths_matrix, Stream_Source_Destination) :
    Streams_paths = [0 for i in range(len(Stream_Source_Destination))]
    n = 0
    for stream in Stream_Source_Destination:
        
        if len(all_paths_matrix[stream[1]][stream[0]]) == 1 : 
            Streams_paths[n]=all_paths_matrix[stream[1]][stream[0]]
            if stream[1] != all_paths_matrix[stream[1]][stream[0]][0] : 
                Streams_paths[n].append(stream[1])
        else :
            Streams_paths[n]=all_paths_matrix[stream[1]][stream[0]]
        Streams_paths[n].insert(0,stream[0])
        if Streams_paths[n][0] == Streams_paths[n][1]:
            del Streams_paths[n][0]
        n = n +1
    return Streams_paths
Streams_paths = Streams_paths_generator(all_paths_matrix, Stream_Source_Destination)

# Determining the path for each Stream regarding the links
def Streams_links_paths_generator(Streams_paths):
    Streams_links_paths = []
    for stream in Streams_paths :
        print(stream[1:])
        n = 1
        stream_allocator = []
        for i in stream[1:]:
            stream_allocator.append([stream[n-1], i])
            n = n+1
        Streams_links_paths.append(stream_allocator)
    return Streams_links_paths
Streams_links_paths = Streams_links_paths_generator(Streams_paths)

# this function generates the link_order_descriptor 
#Basically, the link order descriptor is a list of the index of each link in the path
#from source to destination of a stream #
def Link_order_Descriptor_generator(Streams_links_paths) :
    Link_order_Descriptor = []
    for stream in Streams_links_paths :
        link_order_helper = []
        for link in stream :
            try:
                link_order_helper.append(Network_links.index(tuple(link)))
            except:
                link_order_helper.append(Network_links.index(tuple([link[1],link[0]])))
        Link_order_Descriptor.append(link_order_helper)
    return Link_order_Descriptor
Link_order_Descriptor = Link_order_Descriptor_generator(Streams_links_paths)

# Links per stream, basically is a list that indicates if a link is used for transmitting in a stream

def Links_per_Stream_generator(Network_links, Link_order_Descriptor) : 
    Links_per_Stream = [[0 for link in range(len(Network_links))] for stream in range(len(Link_order_Descriptor))]
    stream_index = 0
    for stream in Link_order_Descriptor :
        for link in stream :
            Links_per_Stream[stream_index][link] = 1
        stream_index = stream_index + 1 
    return Links_per_Stream  

Links_per_Stream = Links_per_Stream_generator(Network_links, Link_order_Descriptor)

########################################################################
########################################################################
###########    Random parameters of the streams    #####################
########################################################################
########################################################################


def Random_Stream_size_and_period_generator(Links_per_Stream): 
    Streams_size = []
    Streams_Period = {}
    for stream_index in range(len(Links_per_Stream)) :
        Streams_size.append(random.sample([1500, 3000, 4500, 6000], 1)) # This is the size of the packages in bytes
        #Streams_size.append(random.sample([6000,9000], 1)) # This is the size of the packages in bytes
        Streams_Period[(stream_index)] = random.sample([200, 400, 800], 1) # This is the period in micro seconds
        #Streams_Period[(stream_index)] = random.sample([100, 200], 1) # This is the period in micro seconds
    #Streams_size = [[7500], [7500]]
    print("#######################Streams_size and Stream Period#################")    
    print(Streams_size)
    print(Streams_Period)
    Streams_Period_list = [(v[0]) for k, v in Streams_Period.items()]
    
    for i in range(len(Streams_Period)):
        Streams_Period[(i)] = Streams_Period[(i)][0]
    print("the same streams_periods but after the funny loop",Streams_Period)
    return Streams_size , Streams_Period, Streams_Period_list
Streams_size , Streams_Period, Streams_Period_list = Random_Stream_size_and_period_generator(Links_per_Stream)

# This funciton reads the periods of the strems and provides the hyperperiod (lcm of all the periods)
def Hyperperiod_generator(Streams_Period_list) :
    Hyperperiod = 1
    for i in Streams_Period_list:
        Hyperperiod = Hyperperiod*i//gcd(Hyperperiod, i)
    return Hyperperiod

Hyperperiod = Hyperperiod_generator(Streams_Period_list)

# This function generates the frames_per_stream, basically a list with the number of frames per stream represented 
# as a set of 1's
# Provides also the maximum number of frames in an stream
def Frames_per_Stream_generator(Streams_size):
    Frames_per_Stream = []
    for repetition in (Streams_size):
        print(repetition[0], type(repetition[0]))
        Frames_per_Stream.append([1 for frame in range(int(float(repetition[0])/1500))])
    
    Max_frames = max([len(frame) for frame in Frames_per_Stream])
    Num_of_Frames = []
    for i in Frames_per_Stream : Num_of_Frames.append(len(i))
    return Frames_per_Stream, Max_frames, Num_of_Frames

Frames_per_Stream, Max_frames, Num_of_Frames = Frames_per_Stream_generator(Streams_size)

# This code generates a matrix that will be used to 
# indicate wheter of not a frame in a stream and in a link exists or not
def Model_Descriptor_generator(Number_of_Streams, Max_frames, Network_links) :
    Model_Descriptor = {}

    for stream in range(Number_of_Streams):
        for frame in range(Max_frames):
            for link in range(len(Network_links)):
                Model_Descriptor[(stream,frame,link)]= 0

    Model_Descriptor_vector = [[[0 for link in range(len(Network_links))] for frame in range(Max_frames)] for stream in range(Number_of_Streams)]

    x = 0
    for stream in Frames_per_Stream:
        y = 0
        for frame in stream:
            z = 0
            for link in Links_per_Stream[x]:
                Model_Descriptor[(x,y,z)] = frame * link 
                Model_Descriptor_vector [x][y][z] = frame * link
                z = z +  1
            y = y + 1
        x = x + 1
    return Model_Descriptor, Model_Descriptor_vector

Model_Descriptor, Model_Descriptor_vector = Model_Descriptor_generator(Number_of_Streams, Max_frames, Network_links)

Streams = range(Number_of_Streams)

# Boolean function that indicates if a combination of Frame Link and Stream exists or not
def frame_exists(Model_Descriptor_vector, stream, frame) :
    return len([*filter(lambda x: x >= 1, Model_Descriptor_vector[stream][frame])])

# Simply, fills the duration of the streams with a fixed value, can be changed in future
def Frame_Duration_generator(Number_of_Streams, Max_frames, Network_links ) :
    Frame_Duration = {}
    for stream in range(Number_of_Streams):
        for frame in range(Max_frames):
            for link in range(len(Network_links)):
                Frame_Duration[(stream,frame,link)]= 12 # This has to be 12
    return Frame_Duration

Frame_Duration = Frame_Duration_generator(Number_of_Streams, Max_frames, Network_links )

# this function creates the deathlines, in this case, all the streams have a fixed deathline
def Deathline_Stream_generator(Frames_per_Stream) :
    Deathline_Stream = {}
    Deathline = 1000 # This is the selected value for the latency deathline
    n = 0

    for stream in range(len(Frames_per_Stream)) :
        Deathline_Stream[(stream)] = Deathline
    return Deathline_Stream 

Deathline_Stream = Deathline_Stream_generator(Frames_per_Stream)

#This function generates the following:

# Repetitions: a vector with all the number of repetitions
# Repetition matrix: a matrix filled with ones regarding the number of repetitions in each stream
# Repetitions Descriptor: a matrix used for determining if a repetition in a determined stream exists or not
# max_repetitions: Simply the maximum number of repetitions in any stream
def Repetitions_generator(Streams_Period) :
    Repetitions = []
    for period in range(len(Streams_Period)):
        Repetitions.append(float(Hyperperiod)/Streams_Period[(period)] - 1)


    Repetitions_Matrix = []
    for repetition in Repetitions :
        Repetitions_Matrix.append([1 for rep in range(int(repetition))])

    print("Getting Repetitions", Repetitions, "and Streams", Streams)
    if max(Repetitions) == 0 :
        Repetitions_Descriptor = [0 for stream in Streams ]
    else :
        Repetitions_Descriptor = [[0 for repetition in range(int(max(Repetitions)))] for stream in Streams ]
    x = 0
    for stream in Repetitions_Matrix:
        y = 0
        for repetition in stream:
            Repetitions_Descriptor[x][y] = repetition * (y+1)
            y = y +1
        x = x + 1
    
    print("looking for:", Repetitions_Descriptor)
    try :
        max_repetitions = max([max(stream) for stream in Repetitions_Descriptor])
    except :
        max_repetitions = 0


    # This is a patch for including the repetition 0 in the constraints 34 and 35
    y = 0
    try :
        for stream in Repetitions_Descriptor :
            x = 0
            for repetition in [stream] :
                #print(y, x)
                if repetition == 0 :
                    Repetitions_Descriptor[y][x] = 9
                x = x +1
            Repetitions_Descriptor[y].insert(0 ,0)
            y = y +1
    except :
        print("Then it is not necessary")
    return Repetitions, Repetitions_Matrix, Repetitions_Descriptor, max_repetitions
Repetitions, Repetitions_Matrix, Repetitions_Descriptor, max_repetitions= Repetitions_generator(Streams_Period)


### Defined unused links
def unused_links_generator(Network_links, Link_order_Descriptor):
    number_of_links = len(Network_links)
    unused_links = []
    for i in range(number_of_links) :
        totalizer = 0
        for link in Link_order_Descriptor:
            print("first flag", link)
            for sub_link in link:
                print("second flag", sub_link, "the number", i)
                if sub_link == i :
                    totalizer = 1
        if totalizer == 0:
            unused_links.append(i)
    print("the hell is happening",unused_links)
    return unused_links
unused_links = unused_links_generator(Network_links, Link_order_Descriptor)
##################################### ILP Model starts here #####################################
# The ILP took as base for this code appears in the paper 
# Optimization algorithms for the scheduling of IEEE 802.1 Time-Sensitive Networking (TSN)
# The authors are Michael Lander and Raagaard Paul Pop

from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.core import Var

model = AbstractModel()
# Sets
model.Streams = Set(initialize= range(Number_of_Streams)) # Num of streams
model.Repetitions = Set(initialize= range(int(max(Repetitions) + 1))) # This is the maximum number of Repetitions
model.Frames = Set(initialize= frozenset(range(Max_frames))) # Maximum number of streams
model.Links = Set(initialize = frozenset(range(len(Network_links)))) # Links Ids

# Parameters
model.Hyperperiod = Param(initialize=Hyperperiod)
model.Large_Number = Param(initialize=9999999999)
model.Max_Syn_Error = Param(initialize=0.00000001)
model.Model_Descriptor = Param(model.Streams, model.Frames, model.Links, initialize= Model_Descriptor)
model.Deathline_Stream = Param(model.Streams, initialize = Deathline_Stream)
model.Period = Param(model.Streams, initialize=Streams_Period)
model.Frame_Duration = Param(model.Streams, model.Frames, model.Links, initialize = Frame_Duration)
model.Num_of_Frames = Param(model.Streams, initialize=Num_of_Frames)

# Variables
model.Frame_Offset = Var(model.Streams, model.Links, model.Frames, within=PositiveIntegers, initialize=1)
model.Aux_Same_Queue = Var(model.Streams, model.Links, model.Streams, within=Binary, initialize=0)
model.Queue_Assignment = Var(model.Streams, model.Links, within=NonNegativeReals, initialize=1)
model.Aux_Var_Dis = Var(model.Streams, model.Frames, model.Streams, model.Frames, model.Links, model.Repetitions, model.Repetitions, within=Binary, initialize = 0)
model.w = Var(model.Streams, model.Frames, model.Streams, model.Frames, model.Links, within=Binary, initialize=0)

#Variables of the Objective Function
model.Lower_Latency = Var(model.Streams, within=NonNegativeReals, initialize=0)
model.Latency = Var(model.Streams, within=Integers, initialize=0)
model.Num_Queues = Var(model.Links, within=PositiveIntegers, initialize=1)

# Before equation 25 there are missing equations, necessaries for reduce the latency 

#Objective Function
def Latency_Num_Queues_rule(model):
    return sum(model.Num_Queues[link] - 1 for link in model.Links )
#    return (0.9) * sum(model.Latency[stream] - model.Lower_Latency[stream] for link in model.Links ) + (0.1) * sum(model.Num_Queues[stream] - 1 for stream in model.Streams )
model.Latency_Num_Queues = Objective(rule=Latency_Num_Queues_rule, sense=minimize)

#Constraints


def Constraint_27_rule(model, stream, link):
    if Model_Descriptor[(stream, 0, link)]:
        print("constaint 27 link", link)
        return model.Num_Queues[link] >= model.Queue_Assignment[stream, link]
    else :
        return Constraint.Skip
model.Constraint_27 = Constraint(model.Streams, model.Links, rule=Constraint_27_rule)

def Constraint_28_rule(model, stream): 
    print("stream", stream, "starting link", Link_order_Descriptor[stream][-1], "last link", Link_order_Descriptor[stream][0])
    return model.Latency[stream] == model.Frame_Offset[stream, Link_order_Descriptor[stream][-1], (len(Frames_per_Stream[stream]) -1) ] + model.Frame_Duration[stream, (len(Frames_per_Stream[stream]) -1) , Link_order_Descriptor[stream][-1] ] - model.Frame_Offset[stream, Link_order_Descriptor[stream][0] , 0 ]
model.Constraint_28 = Constraint(model.Streams, rule=Constraint_28_rule)

def Constraint_29_rule(model, stream):
    return model.Latency[stream] <= model.Deathline_Stream[stream]
model.Constraint_29 = Constraint(model.Streams, rule=Constraint_29_rule)

def Constraint_30_rule(model, stream, frame, link):
    if Model_Descriptor[(stream, frame, link)]:
        print("constaint 30 link", link)
        return model.Frame_Offset[stream, link, frame] <= model.Period[(stream)] - model.Frame_Duration[stream, frame, link]
    else :
        return Constraint.Skip
model.Constraint_30 = Constraint(model.Streams, model.Frames, model.Links, rule=Constraint_30_rule)

def Constraint_31_rule(model, stream, frame, link):
    if Model_Descriptor[(stream, frame, link)] and Link_order_Descriptor[stream].index(link) != 0 :
        print("constaint 31 link", link)
        print("The previous link", Link_order_Descriptor[stream][Link_order_Descriptor[stream].index(link)-1])
        return model.Frame_Offset[stream, link, frame] >= model.Frame_Offset[stream, Link_order_Descriptor[stream][Link_order_Descriptor[stream].index(link)-1],frame] + model.Frame_Duration[stream, frame, Link_order_Descriptor[stream][Link_order_Descriptor[stream].index(link)-1]] + model.Max_Syn_Error
    else :
        return Constraint.Skip
model.Constraint_31 = Constraint(model.Streams, model.Frames, model.Links, rule=Constraint_31_rule)

def Constraint_32_rule(model, stream, frame, link): # This constraint doesn't seems to apply when there is only one frame in the stream
    if Model_Descriptor[(stream, frame, link)] and frame :
        print("constaint 32 link", link)
        print("applying for stream", stream, "frame", frame, "link", link)
        return model.Frame_Offset[stream, link, frame - 1 ] + model.Frame_Duration[stream, frame - 1, link] <= model.Frame_Offset[stream, link, frame]
    else:
        return Constraint.Skip
model.Constraint_32 = Constraint(model.Streams, model.Frames, model.Links, rule=Constraint_32_rule)

def Constraint_34_rule(model, stream, frame, link, stream_2, frame_2, repetition, repetition_2):
    if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream,frame,link)] and Model_Descriptor[(stream_2,frame_2,link)] and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2 :
        print("constaint 34 link", link)
        return Repetitions_Descriptor[stream][repetition] * model.Period[(stream)] + model.Frame_Offset[stream, link, frame] + model.Frame_Duration[stream, frame, link] <= Repetitions_Descriptor[stream_2][repetition_2] * model.Period[(stream_2)] + model.Frame_Offset[stream_2, link, frame_2] +  model.Large_Number * model.Aux_Var_Dis[stream, frame, stream_2, frame_2, link, repetition, repetition_2]
    else:
        return Constraint.Skip
model.Constraint_34 = Constraint(model.Streams, model.Frames, model.Links, model.Streams, model.Frames, model.Repetitions, model.Repetitions, rule=Constraint_34_rule)

def Constraint_35_rule(model, stream, frame, link, stream_2, frame_2, repetition, repetition_2):
    # The constant has to be applied if the combination exists and the frames exists
    if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream,frame,link)] and Model_Descriptor[(stream_2,frame_2,link)] and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
        print("constaint 35 link", link)
        return Repetitions_Descriptor[stream_2][repetition_2] * model.Period[(stream_2)] + model.Frame_Offset[stream_2, link, frame_2] + model.Frame_Duration[stream_2, frame_2, link] <= Repetitions_Descriptor[stream][repetition] * model.Period[(stream)] + model.Frame_Offset[stream, link, frame] + model.Large_Number * (1 - model.Aux_Var_Dis[stream, frame, stream_2, frame_2, link, repetition, repetition_2]) 
    else:
        return Constraint.Skip
model.Constraint_35 = Constraint(model.Streams, model.Frames, model.Links, model.Streams, model.Frames, model.Repetitions, model.Repetitions, rule=Constraint_35_rule)

def Constraint_36_rule(model, stream, frame, link, stream_2, frame_2, repetition, repetition_2 ):
    if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream,frame,link)] and Model_Descriptor[(stream_2,frame_2,link)] and Link_order_Descriptor[stream].index(link) and Link_order_Descriptor[stream_2].index(link) and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
    #if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream,frame,link)] and Model_Descriptor[(stream_2,frame_2,link)] and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
        print("constaint 36 link", link)
        return Repetitions_Descriptor[stream][repetition] * model.Period[stream] + model.Frame_Offset[stream, link, frame] <= Repetitions_Descriptor[stream_2][repetition_2] * model.Period[stream_2] + model.Frame_Offset[stream_2,Link_order_Descriptor[stream][Link_order_Descriptor[stream].index(link)-1], frame_2] + model.Large_Number * (model.w[stream, frame, stream_2, frame_2, link] + model.Aux_Same_Queue[stream, link, stream_2] + model.Aux_Same_Queue[stream_2, link, stream])
    else : 
        return Constraint.Skip
model.Constraint_36 = Constraint(model.Streams, model.Frames, model.Links, model.Streams, model.Frames, model.Repetitions, model.Repetitions, rule=Constraint_36_rule)

def Constraint_37_rule(model, stream, frame, link, stream_2, frame_2, repetition, repetition_2):
    if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream,frame,link)] and Model_Descriptor[(stream_2,frame_2,link)] and Link_order_Descriptor[stream].index(link) and Link_order_Descriptor[stream_2].index(link) and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
    #if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream,frame,link)] and Model_Descriptor[(stream_2,frame_2,link)] and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
        print("constaint 37 link", link)
        return Repetitions_Descriptor[stream_2][repetition_2] * model.Period[stream_2] + model.Frame_Offset[stream_2, link, frame_2] <= Repetitions_Descriptor[stream][repetition] * model.Period[stream] + model.Frame_Offset[stream, Link_order_Descriptor[stream][Link_order_Descriptor[stream].index(link)-1], frame] + model.Large_Number * (1- model.w[stream, frame, stream_2, frame_2, link] + model.Aux_Same_Queue[stream, link, stream_2] + model.Aux_Same_Queue[stream_2, link ,stream])
    else : 
        return Constraint.Skip
model.Constraint_37 = Constraint(model.Streams, model.Frames, model.Links, model.Streams, model.Frames, model.Repetitions, model.Repetitions, rule=Constraint_37_rule)

def Constraint_39_rule(model, stream, link, stream_2):
    if Model_Descriptor[(stream, 0, link)] and Model_Descriptor[(stream_2, 0, link)] and stream != stream_2:
        print("constaint 39 link", link)
        return model.Queue_Assignment[stream_2, link] - model.Queue_Assignment[stream, link] - model.Large_Number * (model.Aux_Same_Queue[stream, link, stream_2] - 1) >= 1 
    else : 
        return Constraint.Skip
model.Constraint_39 = Constraint(model.Streams, model.Links, model.Streams, rule=Constraint_39_rule)

def Constraint_40_rule(model, stream, link, stream_2):
    if Model_Descriptor[(stream, 0, link)] and Model_Descriptor[(stream_2, 0, link)] and stream != stream_2:
        print("constaint 40 link", link)
        return model.Queue_Assignment[stream_2, link] - model.Queue_Assignment[stream, link] - model.Large_Number * model.Aux_Same_Queue[stream, link, stream_2] <= 0
    else : 
        return Constraint.Skip

model.Constraint_40 = Constraint(model.Streams, model.Links, model.Streams, rule=Constraint_40_rule)

def Constraint_41_rule(model, stream, frame, link, stream_2, frame_2, repetition, repetition_2):
    
    if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream, frame, link)] and Model_Descriptor[(stream_2, frame_2, link)] and Link_order_Descriptor[stream].index(link) and Link_order_Descriptor[stream_2].index(link) and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
    #if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream, frame, link)] and Model_Descriptor[(stream_2, frame_2, link)] and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
        print("constaint 41 link", link)
        return  Repetitions_Descriptor[stream][repetition] * model.Period[stream] + model.Frame_Offset[stream, link, frame] + model.Max_Syn_Error <= Repetitions_Descriptor[stream_2][repetition_2] * model.Period[stream_2] + model.Frame_Offset[stream_2,Link_order_Descriptor[stream_2][Link_order_Descriptor[stream_2].index(link)-1], frame_2] + model.Large_Number * (model.w[stream, frame, stream_2, frame_2, link] + model.Aux_Same_Queue[stream, link, stream_2] + model.Aux_Same_Queue[stream_2, link, stream])
    else : 
        return Constraint.Skip
model.Constraint_41 = Constraint(model.Streams, model.Frames, model.Links, model.Streams, model.Frames, model.Repetitions, model.Repetitions, rule=Constraint_41_rule)

def Constraint_42_rule(model, stream, frame, link, stream_2, frame_2, repetition, repetition_2):
    
    if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream, frame, link)] and Model_Descriptor[(stream_2, frame_2, link)] and Link_order_Descriptor[stream].index(link) and Link_order_Descriptor[stream_2].index(link) and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
    #if frame_exists(Model_Descriptor_vector, stream, frame) and frame_exists(Model_Descriptor_vector, stream_2, frame_2) and Model_Descriptor[(stream, frame, link)] and Model_Descriptor[(stream_2, frame_2, link)]  and Repetitions_Descriptor[stream][repetition] != 9 and Repetitions_Descriptor[stream_2][repetition_2] != 9 and stream != stream_2:
        print("This is the error I thing you are looking for", Link_order_Descriptor[stream].index(link))
        print(Link_order_Descriptor[stream])
        print("constaint 42 link", link)
        return Repetitions_Descriptor[stream_2][repetition_2] * model.Period[stream_2] + model.Frame_Offset[stream_2, link, frame_2] + model.Max_Syn_Error <= Repetitions_Descriptor[stream][repetition] * model.Period[stream] + model.Frame_Offset[stream, Link_order_Descriptor[stream][Link_order_Descriptor[stream].index(link)-1], frame] + model.Large_Number * (1 - model.w[stream, frame, stream_2, frame_2, link] + model.Aux_Same_Queue[stream, link, stream_2] + model.Aux_Same_Queue[stream_2, link, stream])
    else : 
        return Constraint.Skip
model.Constraint_42 = Constraint(model.Streams, model.Frames, model.Links, model.Streams, model.Frames, model.Repetitions, model.Repetitions, rule=Constraint_42_rule)

#unused_links_generator(Network_links, Link_order_Descriptor)
def Constraint_reliever_rule(model, link):
    print("constraint reliever", link, unused_links, Link_order_Descriptor, Link_order_Descriptor[0])
    if link in unused_links :
        print("applying for link", link)
        return model.Num_Queues[link] == 1
    else : 
        return Constraint.Skip
model.Constraint_reliever = Constraint(model.Links, rule=Constraint_reliever_rule)

### This part is the creation of the instance in the ilp system
opt = SolverFactory('gurobi')
instance = model.create_instance()
results = opt.solve(instance)
instance.solutions.load_from(results)

#################################################################################
############################## Showing the results ##############################
#################################################################################

print("############### This is the set of offsets ######################")
Result_offsets = []
Clean_offsets = []
Feasibility_indicator = 0
for i in instance.Streams:
    for j in instance.Links:
        for k in instance.Frames:
            if Model_Descriptor_vector [i][k][j] :
                print("The offset of stream", i, "link", j, "frame", k, "is",instance.Frame_Offset[i,j,k].value)
                frame_indicator = ("S", i, "L", j, "F", k)
                helper = { "Task" :str(frame_indicator), "Start": instance.Frame_Offset[i,j,k].value, "Finish" : (instance.Frame_Offset[i,j,k].value +12), "Color" : j }
                clean_offset = { "Task" :str(frame_indicator), "Start": instance.Frame_Offset[i,j,k].value }
                Result_offsets.append(helper)
                Clean_offsets.append(clean_offset)
                if instance.Frame_Offset[i,j,k].value != 1 :
                    Feasibility_indicator = Feasibility_indicator + 1         
print("############### This is the set of latencies ######################")
Results_latencies = []
for stream in instance.Streams:
    print("The latency of Stream", stream, "is",instance.Latency[stream].value)
    Results_latencies.append(instance.Latency[stream].value)
    
print("############### This is the set of queues ######################")
for link in instance.Links:
    print("The number of queues of link ", link, "is",instance.Num_Queues[link].value)
#print(Result_offsets)

print("############### This is the set of queues per stream and link######################")
for stream in instance.Streams:
    for link in instance.Links:
        print("The number of queues of Link",link , "Stream" , stream, "is", instance.Queue_Assignment[stream, link].value)

print("############### This is the set of auxiliar queues variables######################")
for stream in instance.Streams :
    for stream_2 in instance.Streams :
        for link in instance.Links :
            print("Aux variable for stream_1 ", stream, "Stream_2", stream_2, "link", link, ":", instance.Aux_Same_Queue[stream_2, link ,stream].value)

##### For printing the model results and variables #####
#UNCOMMENT if necessary 

# instance.display()
# results.write()
# results.solver.status 
######################## For now on, this code is for generate the Gant chart ########################


def gantt_chart_generator(Result_offsets, Repetitions) :
    data = [[frame['Task'], frame['Start']] for frame in Result_offsets]
    Repetitions = [repetition + 1 for repetition in Repetitions]

    color=['black', 'red', 'green', 'blue', 'cyan', 'magenta', 'fuchsia', 'yellow', 'grey', 'orange', 'pink']

    # This set of code is for generating the repetitions values in the dataset
    #For printing the full gant Chart
    New_offsets = []
    stream_index = 0
    for repetition in Repetitions :
        for frame in Result_offsets:
            substring = "'S', " +  str(stream_index)
            if substring in frame["Task"] :
                for i in range(int(repetition)) :
                    Repeated_Stream = {'Task' : frame["Task"] , 'Start' : frame["Start"] + Streams_Period[stream_index]*(i), 'Color' : color[frame["Color"]]}
                    New_offsets.append(Repeated_Stream)
        stream_index = stream_index + 1

    Result_offsets = New_offsets
    data = [[frame['Task'], frame['Start'], frame['Color']] for frame in New_offsets]
    df = pd.DataFrame(data, columns = ['Process_Name', 'Start', 'Color'])


    # This is for printing the gant Chart 
    plt.subplot(212)
    #plt.figure(figsize=(12, 5))
    plt.barh(y=df.Process_Name, left=df.Start, width=12, color=df.Color)
    plt.grid(axis='x', alpha=0.5)
    plt.ylabel("Frames")
    plt.xlabel("Time in miliseconds")
    plt.title("Gantt Chart")

    return df
df = gantt_chart_generator(Result_offsets, Repetitions)


def information_generator(Num_of_Frames, Streams_Period, Link_order_Descriptor, Network_links, Streams_links_paths):
    #Frames per stream
    #period per stream
    #Links used per stream
    #Network_links
    # Streams_links_paths
    plt.subplot(222)
    plt.text(0.1, 0.9, "Network-links: \n" + str(Network_links), bbox=dict(facecolor='red', alpha=0.5))
    plt.text(0.1, 0.7, "Frames per stream: \n" + str(Num_of_Frames), bbox=dict(facecolor='red', alpha=0.5))
    plt.text(0.1, 0.5, "Streams periods: \n" + str(Streams_Period), bbox=dict(facecolor='red', alpha=0.5))
    plt.text(0.1, 0.3, "Indexed Links order per stream: \n " + str(Link_order_Descriptor), bbox=dict(facecolor='red', alpha=0.5))
    plt.text(0.1, 0.1, "Streams Paths: \n " + str(Streams_links_paths), bbox=dict(facecolor='red', alpha=0.5))
    plt.axis('off')
    plt.show()
information_generator(Num_of_Frames, Streams_Period, Link_order_Descriptor, Network_links, Streams_links_paths)
# Definition of the Data Frame
# Each schedule provides the following:

# Number of Streams 
# Paths of each stream
# Deathline of each Stream
# Periods
# Stream Duration
# Possibility of schedule
# Offset of the frames
# Latencies

Feasibility = False
if Feasibility_indicator > 1 :
    Feasibility = True
Full_scheduled_data = {
    #Parameter of the network 
    "Adjacency_Matrix" : Adjacency_Matrix, 
    #Parameters of the Streams
    "Stream_Source_Destination" : Stream_Source_Destination, 
    "Link_order_Descriptor" : Link_order_Descriptor,
    "Links_per_Stream" : Links_per_Stream, 
    "Number_of_Streams" : len(instance.Streams),
    "Frames_per_Stream" : Frames_per_Stream,
    "Deathline_Stream" : Deathline_Stream,
    "Streams_Period" : Streams_Period,
    #Results
    "Streams_size" : Streams_size,
    "Clean_offsets" : Clean_offsets,
    "Latencies" : Results_latencies,
    "Feasibility" : Feasibility
}


print(Full_scheduled_data)
### This will store the results into a txt for further usage

with open('results.txt', 'a') as f :
    f.write("\n" + str(Full_scheduled_data))
