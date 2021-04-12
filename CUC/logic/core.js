const restconfClient = require('./../restconf-client/restconf-client.js');

let talkerInformation = [];
let listenerInformation = [];
//TODO return chain needs to be done
function receiveDataFromOpcUaServer(receivedData) {
    //Check literally all the contents sent by the server. It must include everyting necessary to generate the correct Groups for the UNI
    if(receivedData.streamId == null) return -1;
    if (receivedData.macAddress == null) return -1;
    if (receivedData.interfaceName == null) return -1;
    if (receivedData.redundancy == null) return -1;
    if (receivedData.maxDelay == null) return -1;
    if (receivedData.vlanCapable == null) return -1;
    if (receivedData.streamIdTypes == null) return -1;
    if (receivedData.identificationTypes == null) return -1;
    if(receivedData.endpointType === "TALKER") {
        if (receivedData.priority == null) return -1;
        if (receivedData.intervalNumerator == null) return -1;
        if (receivedData.intervalDenominator == null) return -1;
        if (receivedData.maxFrameNumber == null) return -1;
        if (receivedData.maxFrameSize == null) return -1;
        if (receivedData.transmissionSelection == null) return -1;
        if (receivedData.earliestTransmitOffset == null) return -1;
        if (receivedData.latestTransmitOffset == null) return -1;
        if (receivedData.jitter == null) return -1;
        talkerInformation.push(receivedData);
    } else{
        listenerInformation.push(receivedData);
    }
    //Check content of streamInformation variable
    checkStreamInformationReady(receivedData.streamId); //ID should be compliant with stream-id-type of the YANG module
}

function checkStreamInformationReady(idStream) {
    //TODO test
    let foundTalker = false;
    let ctrTalker = 0;
    while(!foundTalker && ctrTalker < talkerInformation.length) {
        if(talkerInformation[ctrTalker].streamId === idStream) foundTalker = true;
        else ctrTalker++;
    };
    let foundListener = false;
    let ctrListener = 0;
    while(!foundListener && ctrListener < listenerInformation.length) {
        if(listenerInformation[ctrListener].streamId === idStream) foundListener = true;
        else ctrListener++;
    };
    
    if(foundListener && foundTalker)
    {
        let uniGroups = generateUniGroups(ctrTalker, ctrListener)
        //Once they are ready, send them to the restConfServer (CNC)
        restconfClient.restconfRequest(uniGroups);
        
    }
}

function generateUniGroups(ctrTalker, ctrListener) {
        let streamInformation = {
            "tsn-uni": {
                "stream-list": [{
                    "stream-id": talkerInformation[ctrTalker].streamId,
                    "request": {
                        'talker': {
                            'stream-rank': {
                                'rank':talkerInformation[ctrTalker].priority 
                            },
                            'end-station-interfaces': [{
                                'mac-address': talkerInformation[ctrTalker].macAddress,
                                'interface-name': talkerInformation[ctrTalker].interfaceName
                            }],
                            'traffic-specification': {
                                'interval': {
                                    'numerator': talkerInformation[ctrTalker].intervalNumerator,
                                    'denominator': talkerInformation[ctrTalker].intervalDenominator
                                },
                                'max-frames-per-interval': talkerInformation[ctrTalker].maxFrameNumber,
                                'max-frame-size': talkerInformation[ctrTalker].maxFrameSize,
                                'transmission-selection': talkerInformation[ctrTalker].transmissionSelection,
                                'time-aware': {
                                    'earliest-transmit-offset': talkerInformation[ctrTalker].earliestTransmitOffset,
                                    'latest-transmit-offset': talkerInformation[ctrTalker].latestTransmitOffset,
                                    'jitter': talkerInformation[ctrTalker].jitter
                                }
                            },
                            'user-to-network-requirements': {
                                'num-seamless-trees': talkerInformation[ctrTalker].redundancy,
                                'max-latency': talkerInformation[ctrTalker].maxDelay
                            },
                            'interface-capabilities': { 
                                'vlan-tag-capable': talkerInformation[ctrTalker].vlanCapable,
                                'cb-stream-iden-type-list': talkerInformation[ctrTalker].streamIdTypes,
                                'cb-sequence-type-list': talkerInformation[ctrTalker].identificationTypes
                            }
                        },
                        'listeners-list': [{
                            'end-station-interfaces': [{
                                'mac-address': listenerInformation[ctrListener].macAddress,
                                'interface-name': listenerInformation[ctrListener].interfaceName
                            }],
                            'user-to-network-requirements': {
                                'num-seamless-trees': listenerInformation[ctrListener].redundancy,
                                'max-latency': listenerInformation[ctrListener].maxDelay
                            },
                            'interface-capabilities':  { 
                                'vlan-tag-capable': listenerInformation[ctrListener].vlanCapable,
                                'cb-stream-iden-type-list': listenerInformation[ctrListener].streamIdTypes,
                                'cb-sequence-type-list': listenerInformation[ctrListener].identificationTypes
                            }
                        }]
                    }
                }]
            }
        }
        return streamInformation
}


module.exports.receiveDataFromOpcUaServer = receiveDataFromOpcUaServer;