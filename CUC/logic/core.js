const restconfClient = require('./../restconf-client/restconf-client.js');
const arrayUtils = require('./../utils/arrayUtils.js');
const gateControlListUtils = require('./../utils/gate-control-list/gateControlListUtils');
let talkerInformation = [];
let listenerInformation = [];

let config;

function receiveDataFromOpcUaServer(receivedData) {
    //Check literally all the contents sent by the server. It must include everyting necessary to generate the correct Groups for the UNI
    if(receivedData.request.streamId == null) return -1;
    if (receivedData.request.macAddress == null) return -1;
    if (receivedData.request.interfaceName == null) return -1;
    if (receivedData.request.redundancy == null) return -1;
    if (receivedData.request.maxDelay == null) return -1;
    if (receivedData.request.vlanCapable == null) return -1;
    if (receivedData.request.streamIdTypes == null) return -1;
    if (receivedData.request.identificationTypes == null) return -1;
    if(receivedData.request.endpointType === "TALKER") {
        if (receivedData.request.priority == null) return -1;
        if (receivedData.request.intervalNumerator == null) return -1;
        if (receivedData.request.intervalDenominator == null) return -1;
        receivedData.request.interval = receivedData.request.intervalNumerator / receivedData.request.intervalDenominator;
        if (receivedData.request.maxFrameNumber == null) return -1;
        if (receivedData.request.maxFrameSize == null) return -1;
        if (receivedData.request.transmissionSelection == null) return -1;
        if (receivedData.request.earliestTransmitOffset == null) return -1;
        if (receivedData.request.latestTransmitOffset == null) return -1;
        if (receivedData.request.jitter == null) return -1;
        
        talkerInformation.push(receivedData);
    } else{
        listenerInformation.push(receivedData);
    }
    //Check content of streamInformation variable
    let responseReceived = checkStreamInformationReadyAndSend(receivedData.streamId); //ID should be compliant with stream-id-type of the YANG module
    if(responseReceived) {
        //TODO: parse response into talkerInformation and listenerInformation variables
        let configDataReady = parseConfigurationData();
        if(configDataReady) {
            //Generate gate control list
            let talkerConfig = gateControlListUtils.generateGateControlList(talkerInformation, true);
            let listenerConfig = gateControlListUtils.generateGateControlList(listenerInformation, false);
            //Send the config to endpoints
            talkerConfig['mac-address'];
        } else {
            //TODO: handle errors
        }
    } else {
        //TODO: handle error
    }
}

function checkStreamInformationReadyAndSend(idStream) {
    //TODO test

    let ctrTalker = arrayUtils.indexGetter(talkerInformation, idStream);

    let ctrListener = arrayUtils.indexGetter(listenerInformation, idStream);
    
    if(ctrTalker != -1 && ctrListener != -1)
    {
        let uniGroups = generateUniGroups(ctrTalker, ctrListener)
        //Once they are ready, send them to the restConfServer (CNC)
        restconfClient.restconfRequest(uniGroups);
        //TODO: Maybe the response needs to be polled by a GET with a given stream ID.
        config = require('../utils/yang/json-samples/cncResponse.json');
        return true;
    } else {
        return false;
    }
}

function generateUniGroups(ctrTalker, ctrListener) {
    //Adapt incoming data to UNI definition
    if(talkerInformation[ctrTalker].redundancy) {
        redundancy = 2;
    }
    //Load the UNI instance data to streamInformation
        let streamInformation = {
                "ieee802-dot1q-tsn-types-upc-version:stream-list": {
                    "stream-id": talkerInformation[ctrTalker].request.streamId,
                    "request": {
                        'talker': {
                            'stream-rank': {
                                'rank':talkerInformation[ctrTalker].request.priority 
                            },
                            'end-station-interfaces': [{
                                'mac-address': talkerInformation[ctrTalker].request.macAddress,
                                'interface-name': talkerInformation[ctrTalker].request.interfaceName
                            }],
                            'traffic-specification': {
                                'interval': {
                                    'numerator': talkerInformation[ctrTalker].request.intervalNumerator,
                                    'denominator': talkerInformation[ctrTalker].request.intervalDenominator
                                },
                                'max-frames-per-interval': talkerInformation[ctrTalker].request.maxFrameNumber,
                                'max-frame-size': talkerInformation[ctrTalker].request.maxFrameSize,
                                'transmission-selection': talkerInformation[ctrTalker].request.transmissionSelection,
                                'time-aware': {
                                    'earliest-transmit-offset': talkerInformation[ctrTalker].request.earliestTransmitOffset,
                                    'latest-transmit-offset': talkerInformation[ctrTalker].request.latestTransmitOffset,
                                    'jitter': talkerInformation[ctrTalker].request.jitter
                                }
                            },
                            'user-to-network-requirements': {
                                'num-seamless-trees': talkerInformation[ctrTalker].request.redundancy ? talkerInformation[ctrTalker].request.redundancy = 2 : null,
                                'max-latency': talkerInformation[ctrTalker].request.maxDelay
                            },
                            'interface-capabilities': { 
                                'vlan-tag-capable': talkerInformation[ctrTalker].request.vlanCapable,
                                'cb-stream-iden-type-list': [talkerInformation[ctrTalker].request.streamIdTypes],
                                'cb-sequence-type-list': [talkerInformation[ctrTalker].request.identificationTypes]
                            }
                        },
                        'listeners-list': [{
                            'end-station-interfaces': [{
                                'mac-address': listenerInformation[ctrListener].request.macAddress,
                                'interface-name': listenerInformation[ctrListener].request.interfaceName
                            }],
                            'user-to-network-requirements': {
                                'num-seamless-trees': listenerInformation[ctrListener].request.redundancy ? listenerInformation[ctrListener].request.redundancy = 2 : null,
                                'max-latency': listenerInformation[ctrListener].request.maxDelay
                            },
                            'interface-capabilities':  { 
                                'vlan-tag-capable': listenerInformation[ctrListener].request.vlanCapable,
                                'cb-stream-iden-type-list': [listenerInformation[ctrListener].request.streamIdTypes],
                                'cb-sequence-type-list': [listenerInformation[ctrListener].request.identificationTypes]
                            }
                        }]
                    }
                }
            }
        return streamInformation
}

function parseConfigurationData() {
    let peerStatus = config["ieee802-dot1q-tsn-types-upc-version:stream-list"][0]["configuration"]["status-info"]
    if(peerStatus["failure-code"] != 0) {
    //TODO: handle error codes
    return false;
    }
    else {
        let ctrTalker = arrayUtils.indexGetter(talkerInformation, config["ieee802-dot1q-tsn-types-upc-version:stream-list"]["stream-id"]);
        let ctrListener = arrayUtils.indexGetter(listenerInformation, config["ieee802-dot1q-tsn-types-upc-version:stream-list"]["stream-id"]);
        
        talkerInformation[ctrTalker].config = {
            "latency": config["ieee802-dot1q-tsn-types-upc-version:stream-list"][0]["configuration"]["talker"]["accumulated-latency"],
            "interface-configuration": config["ieee802-dot1q-tsn-types-upc-version:stream-list"][0]["configuration"]["talker"]["interface-configuration"]
        }

        listenerInformation[ctrListener].config = {
            "latency": config["ieee802-dot1q-tsn-types-upc-version:stream-list"][0]["configuration"]["listener-list"][0]["accumulated-latency"],
            "interface-configuration": config["ieee802-dot1q-tsn-types-upc-version:stream-list"][0]["configuration"]["listener-list"][0]["interface-configuration"]
        }
        config = null;
        return true;
    }
    

}

module.exports.receiveDataFromOpcUaServer = receiveDataFromOpcUaServer;