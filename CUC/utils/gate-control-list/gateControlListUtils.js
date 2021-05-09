/**
 * This module is being strictly tested for 1 TSN flow per endpoint.
 * More flows need to be tested / enhancanced by the new code tenant.
 */
var xor = require('buffer-xor');
var bitUtils = require('node-bitarray');
const arrayUtils = require('./../arrayUtils');
const NANOSECONDS = 1000000000;
const MEGA = 1000000;

function computeGCLTalker(list) {
    //From traffic-specification and config response values, a simple GCL can be generated.
    //1 TSN flow escenario. +1 flow scenario is not implemented yet.
    var request, interval, frameSize, frameNumber, vlanTag, timeOffset;
    if(list.streamDetails.length < 2) {
    //Interval = TAS period
        request = list.streamDetails[0].request;
        interval = request.interval;
        frameSize = request.maxFrameSize;
        frameNumber = request.maxFrameNumber;
        let configs = list.streamDetails[0].config['interface-configuration']['interface-list'][0]['config-list'];
        for (let i=0; i<configs.length; i++) {
            switch(Object.keys(configs[i])[1]) {
                case 'ieee802-vlan-tag':
                    vlanTag = configs[i]['ieee802-vlan-tag'];
                    break;
                case 'time-aware-offset':
                    timeOffset = configs[i]['time-aware-offset'];
                    break;
            }
        }
        //With time aware offset, vlan info, traffic specification and interval it is possible to build a GCL for the endpoint.

        //Burst transmit time. 100Mbps assumed = 12.5MBps.
        let timeEmitting = frameSize*frameNumber/(12.5) * NANOSECONDS /  MEGA;

        //Fit it in the interval with time-aware-offset
        let buffer255 = bitUtils.parse(255);
        let bufferPriority7 = bitUtils.parse(128);
        let vlanPriority = bitUtils.parse(1 << vlanTag['priority-code-point']);
        vlanPriority = bitUtils.or(bufferPriority7, vlanPriority);
        interval = interval * NANOSECONDS //Second to ns
        let gateControlList = {
            interval: interval,
            states: [] 
        }
        //Set the gate states in order to permit the 'bitUtils.xor(buffer255, vlanPriority);vlanPriorityId' queue to transmit at that specific time interval.
        gateControlTmp = bitUtils.not(bitUtils.and(buffer255, vlanPriority));
        if(timeOffset<(0.05*interval)) {
            gateControlList.states.push({
                duration: timeEmitting,
                gateStates: vlanPriority
            });
            gateControlList.states.push({
                duration: interval - timeEmitting,
                gateStates: gateControlTmp
            });
            
        } else //Worth it to spend time emitting best effort traffic.
        {
            states.push({
                duration: timeOffset,
                gateStates: gateControlTmp
            });
            states.push({
                duration: timeEmitting,
                gateStates: vlanPriority
            });
            states.push({
                duration: interval - timeOffset - timeEmitting,
                gateStates: vlanPriority
            });            
        }
        //If conflict with other priorities, CBS should be handled. (Possible TODO: )
    console.log("GCL generated")
    return gateControlList;

    } else {
        //1. Get shortest interval
        var ctr = 0;
        interval = 9999999;
        while(ctr < list.streamDetails.length) {
            if(list.streamDetails[ctr].request.interval < interval)
                interval = list.streamDetails[ctr].request.interval;
            ctr++;
        }
        //TODO: 
    }
}

function computeGCLListener(list) {
    var request, interval, frameSize, frameNumber, vlanTag, timeOffset;
    if(list.streamDetails.length < 2) {
    //Interval = TAS period
        request = list.streamDetails[0].request;
        interval = request.interval;
        frameSize = request.maxFrameSize;
        frameNumber = request.maxFrameNumber;
        let configs = list.streamDetails[0].config['interface-configuration']['interface-list'][0]['config-list'];
        for (let i=0; i<configs.length; i++) {
            switch(Object.keys(configs[i])[1]) {
                case 'ieee802-vlan-tag':
                    vlanTag = configs[i]['ieee802-vlan-tag'];
                    break;
                case 'time-aware-offset':
                    timeOffset = configs[i]['time-aware-offset'];
                    break;
            }
        }
        //With time aware offset, vlan info, traffic specification and interval it is possible to build a GCL for the endpoint.

        //Burst transmit time. 100Mbps assumed = 12.5MBps.
        let timeEmitting = frameSize*frameNumber/(12.5) * NANOSECONDS /  MEGA;

        //Fit it in the interval with time-aware-offset
        let buffer255 = bitUtils.parse(255);
        let bufferPriority7 = bitUtils.parse(128);
        let vlanPriority = bitUtils.parse(1 << vlanTag['priority-code-point']);
        vlanPriority = bitUtils.or(bufferPriority7, vlanPriority);
        interval = interval * NANOSECONDS //Second to ns
        let gateControlList = {
            interval: interval,
            states: [] 
        }
        //Set the gate states in order to permit the 'bitUtils.xor(buffer255, vlanPriority);vlanPriorityId' queue to transmit at that specific time interval.
        gateControlTmp = bitUtils.not(bitUtils.and(buffer255, vlanPriority));
        if(timeOffset<(0.05*interval)) {
            gateControlList.states.push({
                duration: timeEmitting,
                gateStates: vlanPriority
            });
            gateControlList.states.push({
                duration: interval - timeEmitting,
                gateStates: gateControlTmp
            });
            
        } else //Worth it to spend time emitting best effort traffic.
        {
            states.push({
                duration: timeOffset,
                gateStates: gateControlTmp
            });
            states.push({
                duration: timeEmitting,
                gateStates: vlanPriority
            });
            states.push({
                duration: interval - timeOffset - timeEmitting,
                gateStates: vlanPriority
            });            
        }
        //If conflict with other priorities, CBS should be handled. (Possible TODO: )
    console.log("GCL generated")
    return gateControlList;

    } else {
        //1. Get shortest interval
        var ctr = 0;
        interval = 9999999;
        while(ctr < list.streamDetails.length) {
            if(list.streamDetails[ctr].request.interval < interval)
                interval = list.streamDetails[ctr].request.interval;
            ctr++;
        }
        //TODO: 
    }
}

function generateGateControlList(streams, isTalker) {
    //Locate same interfaces + name
    let gateControlListArray = [];
    streams.forEach(function(item) {
        //Find MAC in the upper array
        arrayUtils.macCompare(item, gateControlListArray);
    });
    //Compute each element in gateControlListArray
    if(isTalker) {
       for(var i = 0; i<gateControlListArray.length; i++) {
           let gcl = computeGCLTalker(gateControlListArray[i]);
           gateControlListArray[i].gcl = gcl;
       }
    }
    else {
        for(var i = 0; i<gateControlListArray.length; i++)
        computeGCLListener(gateControlListArray[i]);
    }
    return gateControlListArray;
}


module.exports.generateGateControlList = generateGateControlList;
