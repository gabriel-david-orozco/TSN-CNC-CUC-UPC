const opcUaClient = require('./opc-ua-client/opcua-client.js')
const logicHandler = require('./logic/core');
const config = require('./config.json');

const SIMPLE_GCL = 0;
const CBS_GCL = 1;

async function main() {
    //CUC will try to connect to 2 already known servers. To change that, reimplement this file.
    //The result of the content of the servers will be placed in the logic module.
    console.log("Polling Talker features and requirements...");
    let talkerFeatures = await opcUaClient.connectOpcUaServer(config.endpointUrlTalker);
    console.log("Talker information received, waiting for Listener...");
    let listenerFeatures = await opcUaClient.connectOpcUaServer(config.endpointUrlListener);
    console.log("Listener information received. Parsing now both obtained datagroups.");
    
    let streamId = logicHandler.receiveDataFromOpcUaServer(talkerFeatures);
    if(streamId == -1) console.log("Aborting. Obtained TSN configuration is not complete.");
    streamId = logicHandler.receiveDataFromOpcUaServer(listenerFeatures);
    if(streamId == -1) console.log("Aborting. Obtained TSN configuration is not complete.");


    let response = logicHandler.checkStreamInformationReadyAndSend(streamId);

    if(response) {
        logicHandler.generateGclAndSendConfig(SIMPLE_GCL);
    } else {
        "No resonse from CNC. Aborting."
    }
}
main()
