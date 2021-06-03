const opcUaClient = require('./opc-ua-client/opcua-client.js')
const logicHandler = require('./logic/core');
const config = require('./config.json');

async function main() {
    //CUC will try to connect to 2 already known servers. To change that, reimplement this file.
    //The result of the content of the servers will be placed in the logic module.
    console.log("Polling Talker features and requirements...");
    let talkerFeatures = await opcUaClient.connectOpcUaServer(config.endpointUrlTalker);
    console.log("Talker information received, waiting for Listener...");
    let listenerFeatures = await opcUaClient.connectOpcUaServer(config.endpointUrlListener);
    console.log("Listener information received. Parsing now both obtained datagroups.");
    
    let streamId = logicHandler.receiveDataFromOpcUaServer(talkerFeatures);
    streamId = logicHandler.receiveDataFromOpcUaServer(listenerFeatures);

    let response = logicHandler.checkStreamInformationReadyAndSend(streamId);

    if(response) {
        logicHandler.generateGclAndSendConfig();
    } else {
        "No resonse from CNC. Aborting."
    }
}
main()
