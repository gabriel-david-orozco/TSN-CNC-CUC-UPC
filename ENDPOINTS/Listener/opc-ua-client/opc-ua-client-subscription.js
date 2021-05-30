
const opcua = require("node-opcua");

async function connectOpcUaServer(endpointUrl, interval) {
    console.log("Creating subscription: "+interval+" time interval")
    const client = opcua.OPCUAClient.create({
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
    const subscription = opcua.ClientSubscription.create(session, {
        //TODO
        requestedPublishingInterval: interval/1000000,
        requestedLifetimeCount:      100,
        requestedMaxKeepAliveCount:   10,
        maxNotificationsPerPublish:  1,
        publishingEnabled: true,
        priority: 0
    });
    
    subscription.on("started", function() {
        console.log("subscription started for 2 seconds - subscriptionId=", subscription.subscriptionId);
    }).on("keepalive", function() {
        console.log("keepalive");
    }).on("terminated", function() {
       console.log("terminated");
    });

    const monitoredItem  = await subscription.monitor({
        nodeId: opcua.resolveNodeId("ns=1;i=1027"),
        attributeId: opcua.AttributeIds.Value
        },
        {
            samplingInterval: 100,
            discardOldest: true,
            queueSize: 10
        },
        opcua.TimestampsToReturn.Both
    );
    console.log("-------------------------------------");

    monitoredItem.on("changed", function(dataValue) {
        console.log("Received")
        //console.log(dataValue.value.value);
    });
}

module.exports.connectOpcUaServer = connectOpcUaServer;