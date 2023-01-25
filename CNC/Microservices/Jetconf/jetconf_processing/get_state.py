import requests

api_url = "https://127.0.0.1:8443/restconf/data/ieee802-dot1q-tsn-types-upc-version:tsn-uni"
response = requests.get(api_url,auth="/home/jetconf/data/example-client_curl.pem", verify=False)
response.json()