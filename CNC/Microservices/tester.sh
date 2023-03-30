# Okay, this script is for performing the full initialization and testing of the ILP.
# Basically it uses 3 microservices of the full microservices list: The random-generator, preprocessing and ILP
# This will go to generate an aleatory configuration based on the input parameters given in the 
# TSN-CNC-CUC-UPC/CNC/Microservices/Random_generator_microservice/input.conf file
# feel free to change it as you want
# then it will proceed to launch the necessary processes in the next two microservices
# Finally, it will give you two outputs, 
# 1) the image depicting the architecture results and 
# 2) the output parameters of the ILP, including the offsets


# To execute them you can simply run 'bash tester.sh'

docker-compose up -d
sleep 4
docker-compose exec random_generator-microservice bash -c 'python __init__.py'
docker-compose exec preprocessing-microservice bash -c 'python __init__.py'
docker-compose exec ilp bash -c 'source /root/miniconda3/bin/activate base && python __init__.py'
sleep 4
docker-compose down

# Make sure that the code is working for the random generated parameters,
# You will see it at the end of the workflow in an output that says Feasibility: True
# If it says false discard the test and run it again

# You will find the results in the ILP folder (results.txt, testing.png), this folder is mounted to the ILP
# Container so once you rerun the code those files will be overwriten,
# better to safe them in a safe place is you wish to maintain them

# When I wrote this code, there were some specifications completely dependable on the specific use cases, so for some scenarios
# It may not work, simply re run the script until it works