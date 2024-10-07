import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

url = "https://app.geckoterminal.com/api/p1/solana/pools?include=tokens&page=2"

# proxyModeUrl = "http://e2e4f62d5bd34d10a8948fb30d6fb4c29b6245cad02:@proxy.scrape.do:8080"
proxyModeUrl = "http://scraperapi:ffe5edd885677207e089296088cdabab@proxy-server.scraperapi.com:8001"

proxies = {
    "http": proxyModeUrl,
    "https": proxyModeUrl,
}

response = requests.request("GET", url, proxies=proxies, verify=False)

raw_data = response.json()
filtered_data = [
    {
        'attributes': {
            'token_value_data': item['attributes']['token_value_data'],
            'address': item['attributes']['address']
        }
    }
    for item in raw_data['data']
]
filtered_included = [
    {
        'attributes': {
            'address': item['attributes']['address']
        },
        'id': item['id'],
        'type': item['type']
    }
    for item in raw_data['included']
]
raw_data['data'] = filtered_data
raw_data['included'] = filtered_included
print(raw_data)
