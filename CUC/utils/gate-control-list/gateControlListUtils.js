const arrayUtils = require('./../arrayUtils');

function computeGCLTalker(list) {
    //From traffic-specification and config response values, a simple GCL can be generated.
    //1. Get shortest interval
    var ctr = 0;
    var interval = 999999999999;
    while(ctr < list.streamDetails.length) {
        if(list.streamDetails[ctr].request.interval < interval)
            interval = list.streamDetails[ctr].request.interval;
        ctr++;
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
