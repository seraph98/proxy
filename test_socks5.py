import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

url = "https://app.geckoterminal.com/api/p1/solana/pools?include=tokens&page=2"

token = "e2e4f62d5bd34d10a8948fb30d6fb4c29b6245cad02"

proxyModeUrl = "http://{}:@proxy.scrape.do:8080".format(token)

proxies = {

    "http": proxyModeUrl,

    "https": proxyModeUrl,

}

response = requests.request("GET", url, proxies=proxies, verify=False)

print(response.text)
