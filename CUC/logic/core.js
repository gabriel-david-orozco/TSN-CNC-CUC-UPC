const restconfClient = require('./../restconf-client/restconf-client.js');
let streamInformation; //Where both correct data from Listener and Talker will be held until sent via Restonf

let talkerInformation = [];
let listenerInformation = [];
//TODO return chain needs to be done
function receiveDataFromOpcUaServer(receivedData) {
    //Check literally all the contents sent by the server. It must include everyting necessary to generate the correct Groups for the UNI
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
    checkStreamInformationReady(receivedData.id);
}

function checkStreamInformationReady(idStream) {
    //TODO test
    let foundTalker = false;
    let ctrTalker = 0;
    while(!foundTalker && ctrTalker < talkerInformation.length) {
        if(talkerInformation[ctrTalker].id === idStream) foundTalker = true;
        else ctrTalker++;
    };
    let foundListener = false;
    let ctrListener = 0;
    while(!foundListener && ctrListener < talkerInformation.length) {
        if(listenerInformation[ctrListener].id === idStream) foundListener = true;
        else ctrListener++;
    };
    
    if(foundListener && foundTalker)
    {
        streamInformation = null;
        let uniGroups = generateUniGroups()
        //Once they are ready, send them to the restConfServer (CNC)
        restconfClient.restconfRequest(uniGroups);
        
    }
}

function generateUniGroups() {
        streamInformation['group-talker']['stream-rank'].rank = talkerInformation.priority;
        streamInformation['group-talker']['end-station-interfaces'].push({
            'mac-address': talkerInformation.macAddress,
            'interface-name': talkerInformation.interfaceName
        });
        streamInformation['group-talker']['traffic-specification'] = {
            'interval': {
                'numerator': talkerInformation.intervalNumerator,
                'denominator': talkerInformation.intervalDenominator
            },
            'max-frames-per-interval': talkerInformation.maxFrameNumber,
            'max-frame-size': talkerInformation.maxFrameSize,
            'transmission-selection': talkerInformation.transmissionSelection,
            'time-aware': {
                'earliest-transmit-offset': talkerInformation.earliestTransmitOffset,
                'latest-transmit-offset': talkerInformation.latestTransmitOffset,
                'jitter': talkerInformation.jitter
            }
        };
        streamInformation['group-talker']['user-to-network-requirements'] = {
            'num-seamless-trees': talkerInformation.redundancy,
            'max-latency': talkerInformation.maxDelay
        };
        streamInformation['group-talker']['interface-capabilities'] = { 
            'vlan-tag-capable': talkerInformation.vlanCapable,
            'cb-stream-iden-type-list': talkerInformation.streamIdTypes,
            'cb-sequence-type-list': talkerInformation.identificationTypes
        }

        streamInformation['group-listener']['end-station-interfaces'].push({
            'mac-address': listenerInformation.macAddress,
            'interface-name': listenerInformation.interfaceName
        });
        streamInformation['group-listener']['user-to-network-requirements'] = {
            'num-seamless-trees': listenerInformation.redundancy,
            'max-latency': listenerInformation.maxDelay
        };
        streamInformation['group-listener']['interface-capabilities'] = { 
            'vlan-tag-capable': listenerInformation.vlanCapable,
            'cb-stream-iden-type-list': listenerInformation.streamIdTypes,
            'cb-sequence-type-list': listenerInformation.identificationTypes
        }
        //TODO validate YANG module

}


module.exports.receiveDataFromOpcUaServer = receiveDataFromOpcUaServer;