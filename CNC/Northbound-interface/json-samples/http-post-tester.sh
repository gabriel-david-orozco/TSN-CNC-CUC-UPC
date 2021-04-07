CLIENT_CERT="/jetconf/data/example-client_curl.pem"

echo "--- POST new artist"
POST_DATA="@group-interfaces.json"
POST_DATA='{"group-listener": {"mac-address": "60-F2-62-74-45-F4","interface-name": "eth1"}}'
URL="https://127.0.0.1:8443/restconf/data/ieee802-dot1q-tsn-types:group-interface-id"
curl --http2 -k --cert-type PEM -E $CLIENT_CERT -X POST -d "$POST_DATA" "$URL"
