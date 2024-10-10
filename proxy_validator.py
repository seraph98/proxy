import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify, request
from threading import Thread, Lock
import signal
import sys

# Initialize Flask app
app = Flask(__name__)

# Target URL to validate proxies
target_url = "https://public.jupiterapi.com/quote?inputMint=So11111111111111111111111111111111111111112&outputMint=CcTxKZHqU4E2Tek5gh1GZoPZPHncGFkZ36EVMsgDn6sK&amount=1000&slippageBps=1"

# Global list to store valid proxies and task status
valid_proxies = []
proxy_success_rates = {}
task_status = {
    'last_refresh_time': None,
    'total_checked': 0,
    'valid_count': 0,
}
status_lock = Lock()

# Function to check if a proxy works
def check_proxy(proxy):
    return proxy, True
    # proxies = {
        # "http": proxy,
        # "https": proxy,
    # }

    # try:
        # response = requests.get(target_url, proxies=proxies, timeout=5)
        # if response.status_code == 200:
            # return proxy, True
    # except requests.exceptions.RequestException:
        # return proxy, False  # Ensure to return false if an error occurs

    # return proxy, False  # Ensure to return false if an error occurs

def get_proxies_from_geonode():
    limit = 500
    page = 1
    total = 0
    proxies = []

    while True:
        url = f"https://proxylist.geonode.com/api/proxy-list?speed=fast&limit={limit}&page={page}&sort_by=speed&sort_type=asc"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data['data']:
                proxy_str = f"{item['protocols'][0]}://{item['ip']}:{item['port']}"
                proxies.append(proxy_str)
            total = int(data['total'])
            if total <= limit * (page - 1):
                break
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            break  # Exit if there is an error fetching proxies
        except ValueError as e:
            print(f"Parsing error: {e}")
            break

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

# New API endpoint for task status
@app.route('/task_status', methods=['GET'])
def get_task_status():
    with status_lock:
        return jsonify({
            "status":task_status,
            "proxy_success_rates": proxy_success_rates
            }), 200

# New API endpoint to report proxy success rate
@app.route('/report_proxy', methods=['POST'])
def report_proxy():
    data = request.get_json()
    proxy = data.get('proxy')
    success = data.get('success')  # Expected to be a boolean

    if proxy not in proxy_success_rates:
        proxy_success_rates[proxy] = {'success_count': 0, 'fail_count': 0}

    if success:
        proxy_success_rates[proxy]['success_count'] += 1
    else:
        proxy_success_rates[proxy]['fail_count'] += 1

    return jsonify({'message': 'Proxy success status recorded'}), 200

def calculate_valid_proxies():
    global valid_proxies
    currently_valid = []

    for proxy in valid_proxies:
        # Default to True if not present in proxy_success_rates
        stats = proxy_success_rates.get(proxy, {'success_count': 0, 'fail_count': 0})
        total_attempts = stats['success_count'] + stats['fail_count']

        # Calculate the success rate if there are attempts made
        if total_attempts > 10:
            success_rate = stats['success_count'] / total_attempts
            # Only filter out if success_rate < 0.8
            if success_rate >= 0.8:
                currently_valid.append(proxy)
        else:
            # If total_attempts is 0, we don't filter out the proxy
            currently_valid.append(proxy)

    with status_lock:
        valid_proxies = currently_valid  # Update valid proxies
        task_status['valid_count'] = len(valid_proxies)  # Update valid count


def main():
    global valid_proxies, task_status
    proxies_file = "valid_proxies.txt"
    valid_proxies = load_proxies_from_file(proxies_file)

    # Fetch new proxies
    proxies = get_proxies_from_geonode() + fetch_proxies("http") + fetch_proxies("socks5") + fetch_proxies("socks4")
    proxies = list(set(proxies) | set(valid_proxies))  # Avoid redundancy

    print(f"Fetched {len(proxies)} new proxies.")

    while True:
        currently_valid = []
        task_status['total_checked'] = len(proxies)  # Update total checked
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(check_proxy, proxies)

        for result in results:
            if result is not None:  # Check if result is not None
                proxy, is_valid = result
                if is_valid:
                    currently_valid.append(proxy)
                    print(f"Proxy {proxy} is valid.")
                else:
                    print(f"Proxy {proxy} is not valid.")

        valid_proxies = currently_valid  # Update valid proxies
        # Calculate the current valid proxies based on success rates
        calculate_valid_proxies()

        # Save valid proxies to file
        save_valid_proxies_to_file(proxies_file, valid_proxies)  
        
        with status_lock:
            task_status['last_refresh_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Update last refresh time

        print(f"Valid proxies saved: {len(valid_proxies)}")
        time.sleep(60)  # Adjust the sleep time as needed

def signal_handler(sig, frame):
    print('Exiting gracefully...')
    sys.exit(0)

if __name__ == "__main__":
    # Register SIGINT handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the Flask app in a separate thread
    Thread(target=main).start()
    app.run(host='0.0.0.0', port=5009)

