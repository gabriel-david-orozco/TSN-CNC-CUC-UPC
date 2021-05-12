/*global require,setInterval,console */
const opcua = require("node-opcua");

// Let's create an instance of OPCUAServer
const server = new opcua.OPCUAServer({
    port: 4333, // the port of the listening socket of the server
    resourcePath: "/TSNInterface", // this path will be added to the endpoint resource name
     buildInfo : {
        productName: "TSNTalker",
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
        let streamId = "9a-f4-27-E7-7D-b3:E5-e5";
        let endpointType = "TALKER";
        let macAddress = "000102";
        let interfaceName = "eth0";
        //Traffic requirements
        let redundancy = true;
        let maxDelay = 10;

        let vlanCapable = true;
        let streamIdTypes = 60;
        let identificationTypes = 60;
         //Config retrieved from CUC
         let gcl = [0x08];
         let latency = 40;
         let vlanPrioValue = 7;
         let vlanIdValue = 4567;
        
        namespace.addVariable({
            componentOf: interface,
            browseName: "streamId",
            dataType: "String",
            value: {
                get: function () {
                return new opcua.Variant({dataType: opcua.DataType.String, value: streamId });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "endpointType",
            dataType: "String",
            value: {
                get: function () {
                return new opcua.Variant({dataType: opcua.DataType.String, value: endpointType });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "macAddress",
            dataType: "String",
            value: {
                get: function () {
                return new opcua.Variant({dataType: opcua.DataType.String, value: macAddress });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "interfaceName",
            dataType: "String",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.String, value: interfaceName });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "redundancy",
            dataType: "Boolean",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Boolean, value: redundancy });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "maxDelay",
            dataType: "UInt32",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: maxDelay });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "vlanCapable",
            dataType: "Boolean",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Boolean, value: vlanCapable });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "streamIdTypes",
            dataType: "String",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Int32, value: streamIdTypes });
                }
            }
        });

        namespace.addVariable({
            componentOf: interface,
            browseName: "identificationTypes",
            dataType: "String",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Int32, value: identificationTypes });
                }
            }
        });

        let timeAwareOffset = 40;
        if(endpointType === "TALKER") {
            let priority = 5;
            let intervalNumerator = 1;
            let intervalDenominator = 1;
            let maxFrameNumber = 10;
            let maxFrameSize = 1518;
            let transmissionSelection = 0;
            let earliestTransmitOffset = 10;
            let latestTransmitOffset = 30;
            let jitter = 5;

            //Config retrieved from CUC for Talker
            

            namespace.addVariable({
                componentOf: interface,
                browseName: "priority",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: priority });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "intervalNumerator",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: intervalNumerator });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "intervalDenominator",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: intervalDenominator });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "maxFrameNumber",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: maxFrameNumber });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "maxFrameSize",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: maxFrameSize });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "transmissionSelection",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: transmissionSelection });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "earliestTransmitOffset",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: earliestTransmitOffset });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "latesTransmitOffset",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: latestTransmitOffset });
                    }
                }
            });

            namespace.addVariable({
                componentOf: interface,
                browseName: "jitter",
                dataType: "UInt32",
                value: {
                    get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.UInt32, value: jitter });
                    }
                }
            });
        }

        //Declare InterfaceConfig for retrieved config
        const interfaceConfig = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            browseName: "TSNInterfaceConfig"
        }); 
        namespace.addVariable({
            componentOf: interfaceConfig,
            browseName: "tiemAwareOffset",
            dataType: "UInt32",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Int32, value: timeAwareOffset });
                },
                set: function(value) {
                    timeAwareOffset = value;
                }
            }
        });

        namespace.addVariable({
            componentOf: interfaceConfig,
            browseName: "latency",
            dataType: "UInt32",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Int32, value: latency });
                },
                set: function(value) {
                    latency = value;
                }
            }
        });
        
        namespace.addVariable({ //TODO
            componentOf: interfaceConfig,
            browseName: "gcl",
            dataType: "UInt32",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Byte, arrayType: opcua.VariantArrayType.Array, value: gcl });
                },
                set: function(value) {
                    gcl = value;
                }
            }
        });

        namespace.addVariable({
            componentOf: interfaceConfig,
            browseName: "vlanPrioValue",
            dataType: "UInt32",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Int32, value: vlanPrioValue });
                },
                set: function(value) {
                    vlanPrioValue = value;
                }
            }
        });

        namespace.addVariable({
            componentOf: interfaceConfig,
            browseName: "vlanIdValue",
            dataType: "UInt32",
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Int32, value: vlanIdValue });
                },
                set: function(value) {
                    vlanIdValue = value;
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