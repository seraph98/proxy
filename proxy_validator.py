import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Target URL to validate proxies
target_url = "https://public.jupiterapi.com/quote?inputMint=So11111111111111111111111111111111111111112&outputMint=CcTxKZHqU4E2Tek5gh1GZoPZPHncGFkZ36EVMsgDn6sK&amount=1000&slippageBps=1"

# Global list to store valid proxies
valid_proxies = []

# Function to check if a proxy works
def check_proxy(proxy):
    proxies = {
        "http": proxy,
        "https": proxy,
    }

    try:
        response = requests.get(target_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return proxy, True
    except requests.exceptions.RequestException:
        return proxy, False  # Ensure to return false if an error occurs

    return proxy, False  # Ensure to return false if an error occurs

def get_proxies_from_geonode():
    limit = 500
    page = 1
    total = 0
    proxies = []

    while limit * (page - 1) <= total:
        url = f"https://proxylist.geonode.com/api/proxy-list?speed=fast&limit={limit}&page={page}&sort_by=speed&sort_type=asc"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data['data']:
                proxy_str = f"{item['protocols'][0]}://{item['ip']}:{item['port']}"
                proxies.append(proxy_str)
            total = int(data['total'])
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
        except ValueError as e:
            print(f"解析错误: {e}")
    return proxies

def fetch_proxies(protocol):
    proxy_scrape_url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(proxy_scrape_url)
        response.raise_for_status()
        if protocol == "socks5":
            protocol = "socks5h"
        proxies = [f"{protocol}://{line.strip()}" for line in response.text.strip().split("\n") if line.strip()]
        return proxies
    except requests.RequestException as e:
        print(f"Failed to fetch {protocol} proxies: {e}")
        return []

def load_proxies_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def save_valid_proxies_to_file(filename, valid_proxies):
    with open(filename, 'w') as file:
        for proxy in valid_proxies:
            file.write(f"{proxy}\n")

# New API endpoint serving valid proxies
@app.route('/valid_proxies', methods=['GET'])
def get_valid_proxies():
    return jsonify(valid_proxies), 200

def main():
    global valid_proxies
    proxies_file = "valid_proxies.txt"
    valid_proxies = load_proxies_from_file(proxies_file)

    # Fetch new proxies
    proxies = get_proxies_from_geonode() + fetch_proxies("http") + fetch_proxies("socks5") + fetch_proxies("socks4")
    proxies = list(set(proxies) | set(valid_proxies))  # Remove already valid proxies to avoid redundancy

    print(f"Fetched {len(proxies)} new proxies.")

    while True:
        # Use ThreadPoolExecutor for concurrent proxy checks
        valid_proxies_temp = valid_proxies.copy()  # Create a temporary list of valid proxies
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(check_proxy, proxies)

        for result in results:
            if result is not None:  # Check if result is not None
                proxy, is_valid = result
                if is_valid:
                    print(f"Proxy {proxy} is valid.")
                    if proxy not in valid_proxies_temp:  # Avoid duplicates
                        valid_proxies_temp.append(proxy)
                else:
                    print(f"Proxy {proxy} is not valid.")
            else:
                print("Received None from check_proxy, skipping...")

        valid_proxies = valid_proxies_temp  # Update valid proxies
        save_valid_proxies_to_file(proxies_file, valid_proxies)  # Save valid proxies to file
        print(f"Valid proxies saved: {len(valid_proxies)}")

        # Sleep for some time before the next iteration
        time.sleep(5)  # Adjust the sleep time as needed

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    from threading import Thread
    Thread(target=main).start()
    app.run(host='0.0.0.0', port=5009)  # 在5000端口启动Flask服务
