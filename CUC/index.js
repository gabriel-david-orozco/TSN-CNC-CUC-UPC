const opcUaClient = require('./opc-ua-client/opcua-client.js')
const endpointUrlTalker = "opc.tcp://localhost:4333/TSNInterface"; //TODO set up both urls and ports for both endpoints
const endpointUrlListener = "opc.tcp://localhost:4334/TSNInterface"; //TODO set up both urls and ports for both endpoints


//CUC will try to connect to 2 already known servers. To change that, reimplement this file.
//The result of the content of the servers will be placed in the logic module.
opcUaClient.connectOpcUaServer(endpointUrlTalker);
opcUaClient.connectOpcUaServer(endpointUrlListener);