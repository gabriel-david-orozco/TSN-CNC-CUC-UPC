CLIENT_CERT="/home/jetconf/data/example-client_curl.pem"

echo "--- POST new artist"
POST_DATA="@Post-testing.json"
URL="https://127.0.0.1:8443/restconf/data/ieee802-dot1q-tsn-types-upc-version:tsn-uni"
curl --http2 -k --cert-type PEM -E $CLIENT_CERT -X POST -d "$POST_DATA" "$URL"
