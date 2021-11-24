# TSN-CNC-CUC-UPC
Time-Sensitive-Networking Controller developed by EETAC-UPC

This Time Sensitive Networking Controller is developed by the Universitat Politècnica de Catalunya - Escola d'Enginyeria de Telecomunicació i Aeroespacial de Castelldefels following the directions of the IEEE 802.1Qcc IEEE Standard for Local and Metropolitan Area Networks--Bridges and Bridged Networks

# Workflow guide:
- [ ] Translate the microservices of the ILP into two microservices
- [ ] Implement the VLAN_configurator
- [ ] Create a document with interfaces between communications
- [ ] Create the kubernetes cluster
- [ ] test Jetconf with a generated payload
- [ ] Finish the Jetconf integration with the CUC
- [ ] Implement the Soth_configurator microservice
- [ ] We have decided to use RabbitMQ for the messages 


# (Specific task) Translate the microservices of the ILP into two microservices
- [X] Write the input variables from the outside at the beginning of the code
- [ ] Create the images for the kubernetes cluster and push them into the repo
        - [ ] Create the Preprocessing microservice image
- [ ] The ILP calculation should be in other microservice

