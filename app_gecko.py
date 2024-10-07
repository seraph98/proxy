# scheduler.py
import requests
import json
import urllib3
import schedule
import time
import os
from scrape import select_scrape_instance

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API和代理配置
url = "https://app.geckoterminal.com/api/p1/solana/pools?include=tokens&page={}"
# 函数：抓取并保存数据
def fetch_and_save_data(page):
    try:
        raw_data = select_scrape_instance().request(url.format(page))
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
        
        # 保存到文件
        file_path = f"data/page_{page}.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(raw_data, file)
        
        print(f"Page {page} data saved successfully.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}")

# 定时任务：抓取数据
def job():
    for page in range(1, 301):  # 从1到300
        try:
            fetch_and_save_data(page)
        except Exception as e:
            print(e)
        time.sleep(5)


if __name__ == "__main__":
    schedule.every(8).hours.do(job)  # 每小时运行一次

    print("Starting the data fetching job...")
    while True:
        schedule.run_pending()
        time.sleep(1)
