let streamInformation; //Where both correct data from Listener and Talker will be held until sent via Restonf

function checkDataFromOpcUaServer(receivedData) {
    //TODO Check literally all the contents sent by the server. It must include everyting necessary to generate the correct Groups for the UNI
    //TODO Add correct data to streamInformation variable.

    //Check content of streamInformation variable
    checkStreamInformationReady();
}

function checkStreamInformationReady() {
    //TODO when the data is explictly defined.

    if(ready) {
        let uniGroups = generateUniGroups()
        //Once they are ready, send them to the restConfServer (CNC)
        
    }
}

function generateUniGroups() {
    this.streamInformation;
    //TODO generate correct JSON/XML instance data from ../../Yang_models/ieee802-dot1q-tsn-types.json
    let uniGroups;
    return uniGroups;
}


module.exports.checkDataFromOpcUaServer = checkDataFromOpcUaServer;