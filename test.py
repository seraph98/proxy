import cloudscraper
import random


proxies = {'http': 'http://brd-customer-hl_d17528bd-zone-unlimited_datacenter9:bs2jge86ws40@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_d17528bd-zone-unlimited_datacenter9:bs2jge86ws40@brd.superproxy.io:22225'}
def generate_random_parameters():
    browsers = ['chrome', 'firefox']
    platforms = ['linux', 'windows', 'darwin', 'android', 'ios']
    
    parameters = {
        "browser": random.choice(browsers),
        "mobile": random.choice([True, False]),
        "desktop": random.choice([True, False]),
        "platform": random.choice(platforms)
    }

    return parameters
i = 0

while i < 10:
    scraper = cloudscraper.create_scraper(browser="firefox")  # returns a CloudScraper instance
    print(scraper.user_agent.platform)
    print(scraper.user_agent.browser)
    print(scraper.user_agent.mobile)
    print(scraper.user_agent.desktop)
    print('-----')
    print(scraper.get("https://app.geckoterminal.com/api/p1/solana/pools?include=tokens&page=2").text)
    i = i+1




