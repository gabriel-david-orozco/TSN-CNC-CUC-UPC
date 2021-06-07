/**
 * This module is being strictly tested for 1 TSN flow per endpoint.
 * More flows need to be tested / enhancanced by the new code tenant.
 */
const arrayUtils = require('./../arrayUtils');
const NANOSECONDS = 1000000000;
const MEGA = 1000000;

function computeGCLTalker(list) {
    //From traffic-specification and config response values, a simple GCL can be generated.
    //1 TSN flow escenario. +1 flow scenario is not implemented yet.
    //Current used Network Interfaces handle up to 3 different priorities.
    var request, interval, frameSize, frameNumber, vlanTag, timeOffset;
    if(list.streamDetails.length < 2) {
    //Interval = TAS period
        request = list.streamDetails[0].request;
        interval = request.interval;
        frameSize = request.maxFrameSize;
        frameNumber = request.maxFrameNumber;
        let configs = list.streamDetails[0].config['interface-configuration']['interface-list'][0]['config-list'];
        let latency = list.streamDetails[0].config.latency;
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

        //Burst transmit time. 1000Mbps assumed = 125MBps.
        let timeEmitting = frameSize*frameNumber/(125) * NANOSECONDS /  MEGA;
        if(timeEmitting < 0.1*NANOSECONDS ) timeEmitting = 0.1*NANOSECONDS;
        console.log(timeEmitting);
        //Fit it in the interval with time-aware-offset
        let vlanPriority =  vlanTag['priority-code-point'];
        interval = interval * NANOSECONDS //Second to ns
        console.log(interval)
        
        let gateControlList = {
            interval: interval,
            states: [],
            duration: []
        }
        //Set the gate states in order to permit the 'vlanPriorityId' queue to transmit at that specific time interval.
        if(timeOffset<(0.05*interval)) {
            gateControlList.states.push(vlanPriority);
            gateControlList.duration.push(timeEmitting);

            gateControlList.states.push(5);
            gateControlList.duration.push(interval - timeEmitting);
            
        } else //Worth it to spend time emitting best effort traffic.
        {
            gateControlList.states.push(vlanPriority);
            gateControlList.duration.push(timeEmitting);

            gateControlList.states.push(5);
            gateControlList.duration.push(interval - timeEmitting);
            /*
            gateControlList.states.push(gateControlTmp);
            gateControlList.duration.push(timeOffset);

            gateControlList.states.push(vlanPriority);
            gateControlList.duration.push(timeEmitting);
 
            gateControlList.states.push(gateControlTmp);
            gateControlList.duration.push(interval - timeOffset - timeEmitting); */       
        }
        //If conflict with other priorities, CBS should be handled. (Possible TODO: )
    console.log("GCL generated")
    console.log(gateControlList.states);
    console.log(gateControlList.duration);
    let talkerConfig = {
        gcl: gateControlList,
        vlanId: vlanTag['vlan-id'],
        streamId: request.streamId,
        interface: request.interfaceName,
        macAddress: request.macAddress,
        timeOffset: timeOffset,
        latency: latency
    }
    

    return talkerConfig;

    } else {
        //1. Get shortest interval
        var ctr = 0;
        interval = 9999999;
        while(ctr < list.streamDetails.length) {
            if(list.streamDetails[ctr].request.interval < interval)
                interval = list.streamDetails[ctr].request.interval;
            ctr++;
        }
        
    }
}

function generateGateControlList(streams, gclType) {
    //Locate same interfaces + name
    let gateControlListArray = [];
    streams.forEach(function(item) {
        //Find MAC in the upper array
        arrayUtils.macCompare(item, gateControlListArray);
    });
    //Compute each element in gateControlListArray
       for(var i = 0; i<gateControlListArray.length; i++) {
           let gcl = computeGCLTalker(gateControlListArray[i], gclType);
           gateControlListArray[i] = gcl;
       }
    return gateControlListArray;
}


module.exports.generateGateControlList = generateGateControlList;
