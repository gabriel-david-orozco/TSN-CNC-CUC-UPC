/*global require,setInterval,console */
const opcua = require("node-opcua");
const config = require('../config.json');
//const { exec } = require("child_process");
var sudo = require('sudo-js');
sudo.setPassword('UPC-ptp-2020!')
const data = require('../subscriptionPayload/data.json');



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
function generatePayload() {
    var payload = JSON.stringify(data);
    for(let i =1; i<config.dataLength; i++) {
        payload += JSON.stringify(data);
    }
    return payload;
}
async function configureInterface (interfaceName, gclGates, gclGatesTimeDuration, interval, latency, vlanIdValue) {
    console.log("Handle all process to configure i210 board");
    console.log("Interval: " + interval);
    console.log("GCLGates: " + gclGates);
    console.log("GCLGatesDuration: " + gclGatesTimeDuration)
    console.log("Latency: " + latency);
    console.log("Vlan ID: " + vlanIdValue);

    if(vlanIdValue.value != 1997 ) {
        //TODO: thid device should perform Stream Transformation (modify local VLAN ID to the network's VLAN ID before sending)
        console.log("Stream Transformation should be performed. Consider reconfiguring other elements to use same VLAN ID than this device.")
    }

    //Map OPC UA publish traffic to socket priority 2
    command = ("iptables -t mangle -A POSTROUTING -o "+interfaceName.value+" -p tcp --sport 4333 -j CLASSIFY --set-class 0:2").split(" ");
    await sudo.exec(command);

    //Map best effort priority to socket priority 3
    command = ("iptables -t mangle -A POSTROUTING -o "+interfaceName.value+" -p udp -j CLASSIFY --set-class 0:3").split(" ");
    await sudo.exec(command);

    

    //Prepare qdisc taprio configuration
    let taprio = "tc qdisc replace dev "+interfaceName.value+" parent root handle 100 taprio num_tc 3 map 0 2 1 2 2 2 2 2 2 2 2 2 2 2 2 2 queues 1@0 1@1 2@2 base-time 1536883100000000000";

    for(let i=0; i<gclGates.value.length; i++) {
        taprio = taprio + " sched-entry S "+gclGates.value[i]+" "+gclGatesTimeDuration.value[i];
    }
    taprio = taprio + " clockid CLOCK_TAI";
    
    command = taprio.split(" ");
    await sudo.exec(command);

    //TODO: prepare CBS configuration

    //TODO prepare ETF configuration

    //Done. Wait for Listener subscribing for the TSN flow.

}
async function post_initialize() {
    console.log("initialized");
    //Delete all iptables rules
    //await exec("sudo iptables -t mangle -F");
    var command = "iptables -t mangle -F".split(" ");
    await sudo.exec(command);

    //await exec("sudo iptables -X");
    command = "iptables -X".split(" ");
    await sudo.exec(command);
    
    async function construct_my_address_space(server) {
    
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
        
        //Delete all qdisc configurations on device
        //await exec("sudo tc qdisc del dev "+interfaceName+"root");
        command = ("tc qdisc del dev "+interfaceName.value+"root").split(" ");
        await sudo.exec(command);
        
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


        //Talker specific variables
        //let timeAwareOffset = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 40});
        let priority = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 5});
        let intervalNumerator = new opcua.Variant({dataType: opcua.DataType.UInt32, value: config.interval});
        let intervalDenominator = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 1});

        
        
        let maxFrameSize = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 1518});
        let maxFrameNumber = config.dataLength / maxFrameSize.value;
        maxFrameNumber = new opcua.Variant({dataType: opcua.DataType.UInt32, value: Math.ceil(maxFrameNumber)});

        let transmissionSelection =new opcua.Variant({dataType: opcua.DataType.UInt32, value: 0});
        let earliestTransmitOffset = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 10});
        let latestTransmitOffset = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 30});
        let jitter = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 5});

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
        
        //Config retrieved from CUC for Talker
        let intervalTAS = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 0});
        let gclGates = new opcua.Variant({dataType: opcua.DataType.UInt32, arrayType: opcua.VariantArrayType.Array, value: [0x00]});
        let gclGatesTimeDuration = new opcua.Variant({dataType: opcua.DataType.UInt32, arrayType: opcua.VariantArrayType.Array, value: [0x00]});
        let latency = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 40}); //Information only
        let vlanIdValue = new opcua.Variant({dataType: opcua.DataType.UInt32, value: 1997});

        //Declare InterfaceConfig for retrieved config
        const interfaceConfig = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            browseName: "TSNInterfaceConfig"
        }); 
        const launchConfig = namespace.addMethod(interfaceConfig, {
            browseName: "LaunchConfig"
        });
        launchConfig.bindMethod((inputArguments,context,callback) => {
            configureInterface(interfaceName, gclGates, gclGatesTimeDuration, intervalTAS, latency, vlanIdValue);
            callback(null);
        });
        /*TODO: CBS and ETF configuring */

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
        namespace.addVariable({ 
            componentOf: interfaceConfig,
            browseName: "interval",
            dataType: "UInt32",
            value: {
                get: function () {
                    return intervalTAS;
                },
                set: function(value) {
                    intervalTAS.value = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });
        namespace.addVariable({ 
            componentOf: interfaceConfig,
            browseName: "gclGates",
            dataType: "UInt32",
            value: {
                get: function () {
                    return gclGates;
                },
                set: function(value) {
                    gclGates.value = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });

        namespace.addVariable({ 
            componentOf: interfaceConfig,
            browseName: "gclGatesTimeDuration",
            dataType: "UInt32",
            value: {
                get: function () {
                    return gclGatesTimeDuration;
                },
                set: function(value) {
                    gclGatesTimeDuration.value = value.value;
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
                    vlanIdValue.value = value.value;
                    return opcua.StatusCodes.Good;
                }
            }
        });

        //Object to publish
        //Declare InterfaceConfig for retrieved config
        let rawData = new opcua.Variant({dataType: opcua.DataType.String, value:"INIT"});
        let ctr = 0;
        setInterval(function(){ //TODO calcul data 
            rawData = new opcua.Variant({dataType: opcua.DataType.String, value:ctr + generatePayload()});
            ctr++;
            console.log(rawData.value.length)
            console.log("Changed")
        }, 1*1000)
        const publishObject = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            browseName: "PublishObject"
        }); 
        namespace.addVariable({
            componentOf: publishObject,
            browseName: "publishObjectData",
            dataType: "String",
            value: {
                get: function () {
                    return rawData;
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

module.exports.initServer = server.initialize(post_initialize);