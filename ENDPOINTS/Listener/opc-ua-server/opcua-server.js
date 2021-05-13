/*global require,setInterval,console */
const opcua = require("node-opcua");
const config = require('../config.json');


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
            browseName: "TSNInterface"
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
         //Config retrieved from CUC
         let interval = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 0});
         let gclGates = new opcua.Variant({dataType: opcua.DataType.UInt32, arrayType: opcua.VariantArrayType.Array, value: [0x00]});
         let gclGatesTimeDuration = new opcua.Variant({dataType: opcua.DataType.UInt32, arrayType: opcua.VariantArrayType.Array, value: [0x00]});
         let latency = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 40});
         let vlanIdValue = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 4567});
        
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

        //let timeAwareOffset = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 40});
        if(endpointType.value === "TALKER") {
            let priority = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 5});
            let intervalNumerator = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 1});
            let intervalDenominator = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 1});
            let maxFrameNumber = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 10});
            let maxFrameSize = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 1518});
            let transmissionSelection =new opcua.Variant({dataType: opcua.DataType.UInt32, value: 0});
            let earliestTransmitOffset = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 10});
            let latestTransmitOffset = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 30});
            let jitter = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 5});

            //Config retrieved from CUC for Talker
            

            namespace.addVariable({
                componentOf: interface,
                browseName: "priority",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return priority;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "intervalNumerator",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return intervalNumerator;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "intervalDenominator",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return intervalDenominator;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "maxFrameNumber",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return maxFrameNumber;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "maxFrameSize",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return maxFrameSize;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "transmissionSelection",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return transmissionSelection;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "earliestTransmitOffset",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return earliestTransmitOffset;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "latesTransmitOffset",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return latestTransmitOffset;
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "jitter",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return jitter;
                    }
                }
            });
        }

        //Declare InterfaceConfig for retrieved config
        const interfaceConfig = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            browseName: "TSNInterfaceConfig"
        }); 
        /*namespace.addVariable({
            componentOf: interfaceConfig,
            browseName: "timeAwareOffset",
            dataType: "UInt32",
            value: {
                get: function () {
                    return timeAwareOffset;
                },
                set: function(value) {
                    timeAwareOffset = value;
                    return opcua.StatusCodes.Good;
                }
            }
        });*/

        namespace.addVariable({
            componentOf: interfaceConfig,
            browseName: "latency",
            dataType: "UInt32",
            value: {
                get: function () {
                    return latency;
                },
                set: function(value) {
                    latency = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });
        namespace.addVariable({ //TODO
            componentOf: interfaceConfig,
            browseName: "interval",
            dataType: "UInt32",
            value: {
                get: function () {
                    return interval;
                },
                set: function(value) {
                    interval = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });
        namespace.addVariable({ //TODO
            componentOf: interfaceConfig,
            browseName: "gclGates",
            dataType: "UInt32",
            value: {
                get: function () {
                    return gclGates;
                },
                set: function(value) {
                    gclGates = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({ //TODO
            componentOf: interfaceConfig,
            browseName: "gclGatesTimeDuration",
            dataType: "UInt32",
            value: {
                get: function () {
                    return gclGatesTimeDuration;
                },
                set: function(value) {
                    gclGatesTimeDuration = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({
            componentOf: interfaceConfig,
            browseName: "vlanIdValue",
            dataType: "UInt32",
            value: {
                get: function () {
                    console.log(vlanIdValue)
                    return vlanIdValue;
                },
                set: function(value) {
                    vlanIdValue = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });

    }
    construct_my_address_space(server);
    server.start(function() {
        console.log("Server is now listening ... ( press CTRL+C to stop)");
        console.log("port ", server.endpoints[0].port);
        const endpointUrl = server.endpoints[0].endpointDescriptions()[0].endpointUrl;
        console.log(" the primary server endpoint url is ", endpointUrl );
    });
}
server.initialize(post_initialize);