const opcUaClient = require('./opc-ua-client/opcua-client.js')
const endpointUrlTalker = "opc.tcp://urlServer:port"; //TODO set up both urls and ports for both endpoints
const nodeIdTalker = "ns=7;s=Scalar_Simulation_Double"; //TODO set namespace index and identifier. SET UP in server, edit this one as result.
const endpointUrlListener = "opc.tcp://urlServer:port"; //TODO set up both urls and ports for both endpoints
const nodeIdListener = "ns=7;s=Scalar_Simulation_Double"; //TODO set namespace index and identifier. SET UP in server, edit this one as result.


//CUC will try to connect to 2 already known servers. To change that, reimplement this file.
//The result of the content of the servers will be placed in the logic module.
opcUaClient.connectOpcUaServer(endpointUrlTalker);
opcUaClient.connectOpcUaServer(endpointUrlListener);