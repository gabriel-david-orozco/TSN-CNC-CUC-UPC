const logicHandler = require('../logic/core.js');
const {
    OPCUAClient,
    AttributeIds,
    TimestampsToReturn,
    StatusCodes,
    DataType
} = require("node-opcua");

async function connectOpcUaServer(endpointUrl) {
    const client = OPCUAClient.create({
        endpoint_must_exist: false,
        connectionStrategy: { //TODO check connection strategy since another connection handling may be performed.
            maxRetry: 0,
            initialDelay: 2000,
            maxDelay: 10 * 1000
        }
    });
    client.on("backoff", () => console.log("retrying connection")); //Bad case definition

    await client.connect(endpointUrl);

    const session = await client.createSession(); 
    const streamId = await session.readVariableValue("ns=1;i=1001")
    const endpointType = await session.readVariableValue("ns=1;i=1002");
    const macAddress = await session.readVariableValue("ns=1;i=1003");
    const interfaceName = await session.readVariableValue("ns=1;i=1004");
    const redundancy = await session.readVariableValue("ns=1;i=1005");
    const maxDelay = await session.readVariableValue("ns=1;i=1006");
    const vlanCapable = await session.readVariableValue("ns=1;i=1007");
    const streamIdTypes = await session.readVariableValue("ns=1;i=1008");
    const identificationTypes = await session.readVariableValue("ns=1;i=1009");
    

    if(endpointType.value.value === "TALKER") {
        //Talker has more variables received
        const priority = await session.readVariableValue("ns=1;i=1010");
        const intervalNumerator = await session.readVariableValue("ns=1;i=1011");
        const intervalDenominator = await session.readVariableValue("ns=1;i=1012");
        const maxFrameNumber = await session.readVariableValue("ns=1;i=1013");
        const maxFrameSize = await session.readVariableValue("ns=1;i=1014");
        const transmissionSelection = await session.readVariableValue("ns=1;i=1015");
        const earliestTransmitOffset = await session.readVariableValue("ns=1;i=1016");
        const latestTransmitOffset = await session.readVariableValue("ns=1;i=1017");
        const jitter = await session.readVariableValue("ns=1;i=1018");

        dataValue = {
            request: {
                streamId: streamId.value.value,
                endpointType: endpointType.value.value,
                macAddress: macAddress.value.value,
                interfaceName: interfaceName.value.value,
                redundancy: redundancy.value.value,
                maxDelay: maxDelay.value.value,
                vlanCapable: vlanCapable.value.value,
                streamIdTypes: streamIdTypes.value.value,
                identificationTypes: identificationTypes.value.value,
                priority: priority.value.value,
                intervalNumerator: intervalNumerator.value.value,
                intervalDenominator: intervalDenominator.value.value,
                maxFrameNumber: maxFrameNumber.value.value,
                maxFrameSize: maxFrameSize.value.value,
                transmissionSelection: transmissionSelection.value.value,
                earliestTransmitOffset: earliestTransmitOffset.value.value,
                latestTransmitOffset: latestTransmitOffset.value.value,
                jitter: jitter.value.value
            }
        };
    } else {
        dataValue = {
            request: {
                streamId: streamId.value.value,
                endpointType: endpointType.value.value,
                macAddress: macAddress.value.value,
                interfaceName: interfaceName.value.value,
                redundancy: redundancy.value.value,
                maxDelay: maxDelay.value.value,
                vlanCapable: vlanCapable.value.value,
                streamIdTypes: streamIdTypes.value.value,
                identificationTypes: identificationTypes.value.value
            }      
         };
    }
    

    logicHandler.receiveDataFromOpcUaServer(dataValue);
}
async function sendConfigToEndpoints(endpointUrl, config, isTalker) {
    const client = OPCUAClient.create({
        endpoint_must_exist: false,
        connectionStrategy: { //TODO check connection strategy since another connection handling may be performed.
            maxRetry: 0,
            initialDelay: 2000,
            maxDelay: 10 * 1000
        }
    });
    client.on("backoff", () => console.log("retrying connection")); //Bad case definition

    await client.connect(endpointUrl);

    const session = await client.createSession();
    if(isTalker) {
        //TODO: write all talker variables in servers
        await session.writeSingleNode("ns=1;i=1021", {
            dataType: "UInt32",
            value: config[0].latency
        });
        await session.writeSingleNode("ns=1;i=1022", {
            dataType: "UInt32",
            value: config[0].gcl.interval
        });
        await session.writeSingleNode("ns=1;i=1023", {
            dataType: "UInt32",
            arrayType: "Array",
            value: config[0].gcl.states
        });
        await session.writeSingleNode("ns=1;i=1024", {
            dataType: "UInt32",
            arrayType: "Array",
            value: config[0].gcl.duration
        });
        await session.writeSingleNode("ns=1;i=1025", {
            dataType: "UInt32",
            value: config[0].vlanId
        });

        await session.call({objectId: "ns=1;i=1019",
            methodId: "ns=1;i=1020"})
    } else {
        //TODO: write all listener variables in servers
        await session.writeSingleNode("ns=1;i=1012", {
            dataType: "UInt32",
            value: config[0].latency
        });
        await session.writeSingleNode("ns=1;i=1013", {
            dataType: "UInt32",
            value: config[0].gcl.interval
        });
        await session.writeSingleNode("ns=1;i=1014", {
            dataType: "UInt32",
            arrayType: "Array",
            value: config[0].gcl.states
        });
        await session.writeSingleNode("ns=1;i=1015", {
            dataType: "UInt32",
            arrayType: "Array",
            value: config[0].gcl.duration
        });
        await session.writeSingleNode("ns=1;i=1016", {
            dataType: "UInt32",
            value: config[0].vlanId
        });
        await session.call({objectId: "ns=1;i=1010",
            methodId: "ns=1;i=1011"})
    }
}

module.exports.connectOpcUaServer = connectOpcUaServer;
module.exports.sendConfigToEndpoints = sendConfigToEndpoints;