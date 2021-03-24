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

    const browseResult = await session.browse("RootFolder"); //TODO check and compare this line and next one with the server. What is a RootFolder? Root directory of the adress space?
    console.log(browseResult.references.map((r) => r.browseName.toString()).join("\n"));

    //Reading values. In our scenario it should just request all the needed data in Network Requirements section
    const dataValue = await session.read({ nodeId, attributeId: AttributeIds.Value });
    console.log(` value = ${dataValue.value.value.toString()}`);
    logicHandler.receiveDataFromOpcUaServer(dataValue);
    //TODO Subscription to some content. Not yet considered
    /*
    const subscription = await session.createSubscription2({
        requestedPublishingInterval: 1000,
        requestedLifetimeCount: 100, // 1000ms *100 every 2 minutes or so
        requestedMaxKeepAliveCount: 10,// every 10 seconds
        maxNotificationsPerPublish: 10,
        publishingEnabled: true,
        priority: 10
    });

    subscription
        .on("started", () => console.log("subscription started - subscriptionId=", subscription.subscriptionId))
        .on("keepalive", () => console.log("keepalive"))
        .on("terminated", () => console.log("subscription terminated"));
    const monitoredItem = await subscription.monitor({
        nodeId: nodeId,
        attributeId: AttributeIds.Value
    },
        {
            samplingInterval: 1000,
            discardOldest: true,
            queueSize: 10
        }, TimestampsToReturn.Both);


    monitoredItem.on("changed", (dataValue) =>
        console.log(` value = ${dataValue.value.value.toString()}`));

    await subscription.terminate();
    */
}

module.exports.connectOpcUaServer = connectOpcUaServer;