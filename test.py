import cloudscraper

proxies = {'http': 'http://brd-customer-hl_d17528bd-zone-unlimited_datacenter9:bs2jge86ws40@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_d17528bd-zone-unlimited_datacenter9:bs2jge86ws40@brd.superproxy.io:22225'}
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
print(scraper.get("https://app.geckoterminal.com/api/p1/solana/pools?include=tokens&page=2",proxies=proxies).text)  
# print(scraper.get("https://app.geckoterminal.com/api/p1/solana/pools?include=tokens&page=2").text)  
