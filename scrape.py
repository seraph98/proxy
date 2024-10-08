import requests
import random
import json
from abc import ABC, abstractmethod
from typing import Any, List  # 导入 Any 类型

class Info():
    def __init__(self, user: str, weight: int):
        self.user = user
        self.weight = weight


# 定义一个抽象基类（接口）
class Scrape(ABC):
    @abstractmethod
    def request(self, url: str)-> Any:
        pass

    @abstractmethod
    def info(self)-> Info:
        pass



class ScrapeProxy(Scrape):
    def __init__(self, proxy: str, info: Info):
        self.proxies = {
                "http": proxy,
                "https": proxy
                }
        self._info = info

    def request(self, url: str):
        response = requests.get(url, proxies=self.proxies, verify=False)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()

    def info(self)-> Info:
        return self._info


# 实现 Rectangle 类
class ScrapeHTTP(Scrape):
    def __init__(self, host: str, key: str, info: Info):
        self.host = host
        self.key = key
        self._info = info

    def request(self, url: str):
        response = requests.request("POST", self.host, headers={
  'Content-Type': 'application/json'}, data=json.dumps({
  "url": url,
  }))
        response.raise_for_status()  # 检查请求是否成功
        return response.json()

    def info(self)-> Info:
        return self._info


scrape_instances: List[Scrape] = [
        ScrapeProxy("http://e2e4f62d5bd34d10a8948fb30d6fb4c29b6245cad02:@proxy.scrape.do:8080", Info("seraph", 1000)),
        ScrapeProxy("http://scraperapi:ffe5edd885677207e089296088cdabab@proxy-server.scraperapi.com:8001", Info("seraph", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "06b251870d68581bde03b817d866a78cb6622141", Info("seraph", 250)),

        ScrapeProxy("http://22dfafa3c7314d78ade014c0bebc371d32601bac799:@proxy.scrape.do:8080", Info("yang", 1000)),
        ScrapeProxy("http://scraperapi:c89235cf4298423fda4a363038029f71@proxy-server.scraperapi.com:8001", Info("yang", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "8c64ef663ee2019ec24d559ca997574b2d4d5fd4", Info("yang", 250)),


        ScrapeProxy("http://266241928c824b93a30606ac3648529c56fb3ba5869:@proxy.scrape.do:8080", Info("yangfeilong.beyond", 1000)),
        ScrapeProxy("http://scraperapi:245d8f5d832c6fc0f74ef3abd248780b@proxy-server.scraperapi.com:8001", Info("yangfeilong.beyond", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "36c9159516b338ea7b65d387dd34594a7d831ea0", Info("yangfeilong.beyond", 250)),
        ]

def select_scrape_instance() -> Scrape:
    # 计算总权重
    total_weight = sum(instance.info().weight for instance in scrape_instances)
    # 生成一个随机数
    random_value = random.uniform(0, total_weight)
    # 确定选择哪个实例
    cumulative_weight = 0
    for instance in scrape_instances:
        cumulative_weight += instance.info().weight
        if random_value <= cumulative_weight:
            return instance
    # 理论上不应该到这里，若把权重设计正确的话
    return random.choice(scrape_instances)
