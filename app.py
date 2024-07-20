from flask import Flask, request

import random

import cloudscraper


app = Flask(__name__)

gecko_base = "https://app.geckoterminal.com"

class ProxyInfo:
    def __init__(self, user, ps):
        self.user = user  # 实例变量
        self.ps = ps   # 实例变量

    def proxy(self):
        return {
                'http': f'http://{self.user}:{self.ps}@brd.superproxy.io:22225',
                'https': f'http://{self.user}:{self.ps}@brd.superproxy.io:22225'
                }

proxy_list = [
ProxyInfo('brd-customer-hl_c1058bfc-zone-hk_center', 'nxz8uq87mzau'),
ProxyInfo('brd-customer-hl_d17528bd-zone-usa_gmail_01', 'puiiflkhl0tz'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter1', 'ywvy74lo79wv'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter2', 'zy47qndq79o9'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter3', '1f9yv389u9e1'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter4', '9iq3sg6ry2yt'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter5', 'qfc5u9v0g074'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter6', 'v77e4s32e9hy'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter7', '0st9m1nzy8ky'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter8', 'vsf9xenxexip'),
ProxyInfo('brd-customer-hl_d17528bd-zone-unlimited_datacenter9', 'bs2jge86ws40'),
        ]

def randProxies():
    return random.choice(proxy_list).proxy()

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
@app.route('/api/p1/solana/pools')
def pools():
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    query = request.full_path
    gecko_url = gecko_base + query
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    raw_data = None  # 初始化 raw_data
    data = None      # 初始化 data
    try:
        raw_data = scraper.get(gecko_url, proxies=randProxies())
        data = raw_data.json()
    except Exception as e:
        print('==========')
        print(gecko_url)
        print(e)
        print('----------')
        print('data:', raw_data)
        print('----------')
        raise
    return data  # => "<!DOCTYPE html><html><head>..."


@app.route('/api/p1/solana/latest_pools')
def latest_pools():
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    query = request.full_path
    gecko_url = gecko_base + query
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    return scraper.get(gecko_url).json()  # => "<!DOCTYPE html><html><head>..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

