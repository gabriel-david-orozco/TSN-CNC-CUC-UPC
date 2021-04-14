CLIENT_CERT="/home/jetconf/data/example-client_curl.pem"

echo "--- POST new artist"
POST_DATA="@Post-testing.json"
URL="https://127.0.0.1:8443/restconf/data/ieee802-dot1q-tsn-types-upc-version:tsn-uni/stream-list=12-5A-99-aC-BF-b4:bC-25"
curl --http2 -k --cert-type PEM -E $CLIENT_CERT -X POST -d "$POST_DATA" "$URL"
