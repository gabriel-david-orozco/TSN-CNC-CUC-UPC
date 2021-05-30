const fs = require('fs');
const path = require('path');
const http2 = require('http2');

var client;


function restconfRequest(body) {
    client= http2.connect('https://127.0.0.1:8443', {
      ca: fs.readFileSync(path.resolve(__dirname, "../resources/ca.pem")),
      cert: fs.readFileSync(path.resolve(__dirname, "../resources/client-certificate.pem")),
      key: fs.readFileSync(path.resolve(__dirname, "../resources/client-key.pem")) 
    });
    client.on('error', (err) => console.error(err));
    let buffer = Buffer.from(JSON.stringify(body));

    const req = client.request({
        ':method': 'POST',
        ':path' : '/restconf/data/ieee802-dot1q-tsn-types-upc-version:tsn-uni',
        'Content-Type': 'application/json',
      });
    
    req.on('response', (headers, flags) => {
      for (const name in headers) {
        console.log(`${name}: ${headers[name]}`);
      }
    });
    
    req.setEncoding('utf8');
    let data = '';
    req.on('data', (chunk) => { data += chunk; });
    req.on('end', () => {
      console.log(`\n${data}`);
      client.close();
    });
    req.write(buffer);
    req.end();
}

module.exports.restconfRequest = restconfRequest;