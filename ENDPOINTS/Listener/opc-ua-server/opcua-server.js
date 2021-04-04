/*global require,setInterval,console */
const opcua = require("node-opcua");

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
    
        // add some variables
        let macAddress = "HOLA";
        let interfaceName;
        let redundancy;
        let maxDelay;

        let vlanCapable;
        let streamIdTypes;

        //If talker, uncomment this
        //TODO
        
        namespace.addVariable({
            componentOf: interface,
            browseName: "macAddress",
            dataType: "String",
            value: {
                get: macAddress//TODO: implement;
            }
        });

        /*namespace.addVariable({
            componentOf: interfaceName,
            browseName: "interfaceName",
            dataType: "String",
            value: {
                get: getInterfaceName()//TODO: implement;
            }
        });

        namespace.addVariable({
            componentOf: redundancy,
            browseName: "redundancy",
            dataType: "String",
            value: {
                get: getRedundancy()//TODO: implement;
            }
        });

        namespace.addVariable({
            componentOf: maxDelay,
            browseName: "maxDelay",
            dataType: "String",
            value: {
                get: getMaxDelay()//TODO: implement;
            }
        });

        namespace.addVariable({
            componentOf: vlanCapable,
            browseName: "vlanCapable",
            dataType: "String",
            value: {
                get: getVlanCapable()//TODO: implement;
            }
        });

        namespace.addVariable({
            componentOf: streamIdTypes,
            browseName: "streamIdTypes",
            dataType: "String",
            value: {
                get: getStreamIdTypes()//TODO: implement;
            }
        });*/


        /*namespace.addVariable({
        
            componentOf: device,
        
            nodeId: "ns=1;b=1020FFAA", // some opaque NodeId in namespace 4
        
            browseName: "MyVariable2",
        
            dataType: "Double",    
        
            value: {
                get: function () {
                    return new opcua.Variant({dataType: opcua.DataType.Double, value: variable2 });
                },
                set: function (variant) {
                    variable2 = parseFloat(variant.value);
                    return opcua.StatusCodes.Good;
                }
            }
        });*/
        const os = require("os");
        /**
         * returns the percentage of free memory on the running machine
         * @return {double}
         */
        /*function available_memory() {
            // var value = process.memoryUsage().heapUsed / 1000000;
            const percentageMemUsed = os.freemem() / os.totalmem() * 100.0;
            return percentageMemUsed;
        }
        namespace.addVariable({
        
            componentOf: device,
        
            nodeId: "s=free_memory", // a string nodeID
            browseName: "FreeMemory",
            dataType: "Double",    
            value: {
                get: function () {return new opcua.Variant({dataType: opcua.DataType.Double, value: available_memory() });}
            }
        });*/
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