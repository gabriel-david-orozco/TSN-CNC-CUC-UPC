const Client = require('node-rest-client').Client;
 
var client = new Client();

function restconfRequest(data) {
    var args = {
        data: data,
        headers: { "Content-Type": "application/json" }
    };
     
    client.post("URL RESTCONF", args, function (data, response) {
        // parsed response body as js object
        console.log(data);
        // raw response
        console.log(response);
    });
}

module.exports.restconfRequest = restconfRequest;