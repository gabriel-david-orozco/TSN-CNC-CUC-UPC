/**
 * This module is being strictly tested for 1 TSN flow per endpoint.
 * More flows need to be tested / enhancanced by the new code tenant.
 */

const arrayUtils = require('./../arrayUtils');

function computeGCLTalker(list) {
    //From traffic-specification and config response values, a simple GCL can be generated.
    //1 TSN flow escenario. +1 flow scenario is not implemented yet.
    var interval, vlanTag, timeOffset;
    if(list.streamDetails.length < 2) {
        interval = list.streamDetails[0].request.interval;
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

        //Burst transmit time. 100Mbps assumed.

        //Fit it in the interval with time-aware-offset

        //Set the gate states in order to permit the 'vlanPriorityId' queue to transmit at that specific time interval.

        //If conflict with other priorities, CBS should be handled. (Possible TODO: )

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
           computeGCLTalker(gateControlListArray[i]);
       }
    }
    else {
        for(var i = 0; i<gateControlListArray.length; i++)
        computeGCLListener(gateControlListArray[i]);
    }
}


module.exports.generateGateControlList = generateGateControlList;
