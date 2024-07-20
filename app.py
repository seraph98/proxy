from flask import Flask, request
import random
import cloudscraper
import time

app = Flask(__name__)

gecko_base = "https://app.geckoterminal.com"

class ProxyInfo:
    def __init__(self, user, ps):
        self.user = user  # 实例变量
        self.ps = ps      # 实例变量

    def proxy(self):
        return {
            'http': f'http://{self.user}:{self.ps}@brd.superproxy.io:22225',
            'https': f'http://{self.user}:{self.ps}@brd.superproxy.io:22225'
        }

proxy_list = [
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

# 缓存字典
cache = {}
cache_expiry = 300  # 缓存有效期（秒）

@app.route('/api/p1/solana/pools')
def pools():
    query = request.full_path
    gecko_url = gecko_base + query
    
    # 检查缓存
    current_time = time.time()
    if gecko_url in cache:
        cached_data, timestamp = cache[gecko_url]
        if current_time - timestamp < cache_expiry:
            return cached_data  # 返回缓存数据

    # 如果没有缓存或缓存过期，进行请求
    scraper = cloudscraper.create_scraper(browser="chrome")
    proxy = randProxies()
    try:
        raw_data = scraper.get(gecko_url, proxies=proxy).json()
        # 将请求结果和当前时间存入缓存
        cache[gecko_url] = (raw_data, current_time)
    except Exception as e:
        print([scraper.user_agent.platform,scraper.user_agent.browser ])
        print(gecko_url)
        print(e)
        print(proxy)
        raise

    return raw_data

@app.route('/api/p1/solana/latest_pools')
def latest_pools():
    query = request.full_path
    gecko_url = gecko_base + query
    
    # 检查缓存
    current_time = time.time()
    if gecko_url in cache:
        cached_data, timestamp = cache[gecko_url]
        if current_time - timestamp < cache_expiry:
            return cached_data  # 返回缓存数据

    # 如果没有缓存或缓存过期，进行请求
    scraper = cloudscraper.create_scraper(browser="chrome")
    proxy = randProxies()
    try:
        raw_data = scraper.get(gecko_url, proxies=proxy).json()
        # 将请求结果和当前时间存入缓存
        cache[gecko_url] = (raw_data, current_time)
    except Exception as e:
        print(gecko_url)
        print(e)
        print(proxy)
        raise

    return raw_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

