const Yang = require('yang-js');
const fs = require('fs');
const path = require('path');
let rawTsnSchema = require('./ieee802-dot1q-tsn-types.js').schema;
Yang.import(path.resolve(__dirname, "./../../Yang_models/ietf-inet-types.yang"));

//The following schema is just the interface, instance data should be generated.
var schema = Yang.parse(rawTsnSchema);

//TODO create method that validates the input data with the already defined schema
function validateData(instanceData) {
    try {
        schema.validate(instanceData);
        return instanceData;
    } catch(error) {
        console.log("Error on validating the instance data")
        return -1;
    }
}
