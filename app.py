from flask import Flask, request

import cloudscraper


app = Flask(__name__)

gecko_base = "https://app.geckoterminal.com"

proxies = {'http': 'http://brd-customer-hl_d17528bd-zone-unlimited_datacenter9:bs2jge86ws40@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_d17528bd-zone-unlimited_datacenter9:bs2jge86ws40@brd.superproxy.io:22225'}

@app.route('/api/p1/solana/pools')
def pools():
    query = request.full_path
    gecko_url = gecko_base + query
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    data = ''
    raw_data = ''
    try:
        raw_data = scraper.get(gecko_url, proxies=proxies)
        data = raw_data.json()
    except Exception as e:
        print(gecko_url)
        print(e)
        print('raw_data:',raw_data)
        print('data:', data)
        raise
    return data  # => "<!DOCTYPE html><html><head>..."


@app.route('/api/p1/solana/latest_pools')
def latest_pools():
    query = request.full_path
    gecko_url = gecko_base + query
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    return scraper.get(gecko_url).json()  # => "<!DOCTYPE html><html><head>..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

