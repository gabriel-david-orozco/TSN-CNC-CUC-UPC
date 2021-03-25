const Client = require('node-rest-client').Client;
const fs = require('fs');

var options = {
    connection: {
        secureOptions: constants.SSL_OP_NO_TLSv1_2,
        ciphers: 'ECDHE-RSA-AES256-SHA:AES256-SHA:RC4-SHA:RC4:HIGH:!MD5:!aNULL:!EDH:!AESGCM',
        honorCipherOrder: true,
        ca: fs.readFileSync(path.resolve(__dirname, ""))//TODO: include the server certificate (self signed one)
    }
};
var client = new Client(options);

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