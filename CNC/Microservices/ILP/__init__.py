from ILP_Generator import *
from time import time
import os
import json

if __name__ == "__main__":

    preprocessing_flag = os.path.exists('/var/preprocessing.txt')
    if(preprocessing_flag):
       with open('/var/preprocessing.txt') as preprocessing_json_file:
          preprocessing = json.load(preprocessing_json_file)
           # Reading of the input data  
           # Djikstra scheduler
           # The not so easy microservices are the Repetition_Descriptor and the Frame Duration. 
          print("This is the thing you are looking for", preprocessing["Frame_Duration"])
          print("This is the other thing you are looking for \n", preprocessing["Model_Descriptor"])







    else:
        print("There is not input data, check the previous microserrvices or the RabbitMQ logs")
