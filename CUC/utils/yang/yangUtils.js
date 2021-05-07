const Yang = require('yang-js');
const path = require('path');
const talkerListenerJsonSample = require('./json-samples/talker.json');
let rawTsnSchema = require('./ieee802-dot1q-tsn-types.js').schema;
Yang.import(path.resolve(__dirname, "./../../../Yang_models/ietf-inet-types.yang"));
Yang.import(path.resolve(__dirname, "./../../../Yang_models/ietf-yang-types.yang"));
//The following schema is just the interface, instance data should be generated.
var schema = Yang.parse(rawTsnSchema);
validateData(talkerListenerJsonSample);

function validateData(instanceData) {
    try {
        schema.validate(instanceData);
        return instanceData;
    } catch(error) {
        console.log("Error on validating the instance data: " + error)
        return -1;
    }
}