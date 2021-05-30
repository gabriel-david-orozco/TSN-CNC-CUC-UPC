const opcUaClient = require('./opc-ua-client/opcua-client.js')
const logicHandler = require('./logic/core');
const config = require('./config.json');

async function main() {
    //CUC will try to connect to 2 already known servers. To change that, reimplement this file.
    //The result of the content of the servers will be placed in the logic module.
    let talkerFeatures = await opcUaClient.connectOpcUaServer(config.endpointUrlTalker);
    let listenerFeatures = await opcUaClient.connectOpcUaServer(config.endpointUrlListener);
    
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
