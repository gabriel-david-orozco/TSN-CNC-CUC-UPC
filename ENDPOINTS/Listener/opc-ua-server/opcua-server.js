/*global require,setInterval,console */
const opcua = require("node-opcua");
const config = require('../config.json');
const subscriptionClient = require('../opc-ua-client/opc-ua-client-subscription');


// Let's create an instance of OPCUAServer
const server = new opcua.OPCUAServer({
    port: 4334, // the port of the listening socket of the server
    resourcePath: "/TSNInterface", // this path will be added to the endpoint resource name
     buildInfo : {
        productName: "TSNListener",
        buildNumber: "0001",
        buildDate: new Date(2021,4,4)
    }
});

function post_initialize() {
    console.log("initialized");
    function construct_my_address_space(server) {
    
        const addressSpace = server.engine.addressSpace;
        const namespace = addressSpace.getOwnNamespace();
    
        // declare a new object
        const interface = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            browseName: "EndpointFeatures"
        });
    
        // Interface specifications
        let streamId = new opcua.Variant({dataType: opcua.DataType.String, value: config.streamId});
        let endpointType = new opcua.Variant({dataType: opcua.DataType.String, value: config.type});
        let macAddress = new opcua.Variant({dataType: opcua.DataType.String, value: config.macAddress});
        let interfaceName = new opcua.Variant({dataType: opcua.DataType.String, value: config.interface});
        //Traffic requirements
        let redundancy = new opcua.Variant({dataType: opcua.DataType.Boolean, value: false});
        let maxDelay = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 10});

        let vlanCapable = new opcua.Variant({dataType: opcua.DataType.Boolean, value: true});
        let streamIdTypes = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 60});
        let identificationTypes = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 60});
        
        namespace.addVariable({
            componentOf: interface,
            browseName: "streamId",
            dataType: "String",
            value: {
                get: function () {
                return streamId;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "endpointType",
            dataType: "String",
            value: {
                get: function () {
                return endpointType;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "macAddress",
            dataType: "String",
            value: {
                get: function () {
                return macAddress;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "interfaceName",
            dataType: "String",
            value: {
                get: function () {
                    return interfaceName;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "redundancy",
            dataType: "Boolean",
            value: {
                get: function () {
                    return redundancy;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "maxDelay",
            dataType: "UInt32",
            value: {
                get: function () {
                    return maxDelay;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "vlanCapable",
            dataType: "Boolean",
            value: {
                get: function () {
                    return vlanCapable;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "streamIdTypes",
            dataType: "UInt32",
            value: {
                get: function () {
                    return streamIdTypes;
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "identificationTypes",
            dataType: "UInt32",
            value: {
                get: function () {
                    return identificationTypes;
                }
            }
        });


        //Declare SubscriptionObject to manage subscription
        let interval;
        const subscribeClientObject = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            browseName: "SubscribeClientObject"
        }); 
        namespace.addVariable({
            componentOf: subscribeClientObject,
            browseName: "interval",
            dataType: "UInt32",
            value: {
                get: function () {
                    return identificationTypes;
                },
                set: function(intervalValue) {
                    interval = intervalValue.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });
        const launchConfig = namespace.addMethod(subscribeClientObject, {
            browseName: "InitSubscription"
        });
        launchConfig.bindMethod((callback) => {
            //Create opcUA client that requests subcription data and prints it
            subscriptionClient.connectOpcUaServer(config.talkerEndpointUrl, interval);
            return opcua.StatusCodes.Good;
        })

        

    }
    construct_my_address_space(server);
    server.start(function() {
        console.log("Server is now listening ... ( press CTRL+C to stop)");
        console.log("port ", server.endpoints[0].port);
        const endpointUrl = server.endpoints[0].endpointDescriptions()[0].endpointUrl;
        console.log(" the primary server endpoint url is ", endpointUrl );
    });
}

module.exports.initServer = server.initialize(post_initialize);
