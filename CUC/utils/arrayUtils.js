
function indexGetter(array, idStream) {
    let ctr = 0;
    let found = false;
    while(!found && ctr < array.length) {
        if(array[ctr].streamId === idStream) found = true;
        else ctr++;
    };
    if(found) return ctr;
    else return -1;
}

function macCompare(item, list) {
    let ctr = 0;
    let found = false;
    while(ctr < list.length && !found) {
        if(item.config['interface-configuration']['interface-list'][0]['mac-address'] == list[ctr]['mac-address']) 
            found = true;
        else ctr++
    }
    if(found)   list[ctr].streamDetails.push(item);
    else    list.push({'mac-address': item.config['interface-configuration']['interface-list'][0]['mac-address'], 'streamDetails': [item]});
}

module.exports.indexGetter = indexGetter;
module.exports.macCompare = macCompare;