
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

module.exports.indexGetter = indexGetter;