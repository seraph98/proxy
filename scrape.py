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


        ScrapeProxy("http://19d392bb89c7451e9194ed69aa5a22e0c91763c4e3f:@proxy.scrape.do:8080", Info("Anamarcia", 1000)),
        ScrapeProxy("http://scraperapi:2a842e8e29778cb85b852f2594ff056d@proxy-server.scraperapi.com:8001", Info("Anamarcia", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "f2abdfaf8183760fbd7a57d6f5ee059243c230cb", Info("Anamarcia", 250)),


        ScrapeProxy("http://8931a3de1dc848dbbb74e2a0265ba97b6c6ed1f468c:@proxy.scrape.do:8080", Info("seraph_01", 1000)),
        ScrapeProxy("http://scraperapi:8e607b68838d36e5fa16d85a5368bc7f@proxy-server.scraperapi.com:8001", Info("seraph_01", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "34a3a1919964d56ba75942547fc457fdfd494460", Info("seraph_01", 250)),


        ScrapeProxy("http://75948c8e3fa0478497e1ad107ae9778584982607989:@proxy.scrape.do:8080", Info("Fary", 1000)),
        ScrapeProxy("http://scraperapi:e92ae1bd4aaa3642b79020dec1fa5e4a@proxy-server.scraperapi.com:8001", Info("Fary", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "a31d707a72f41dfb07b3aec77f10b0c32b8a3503", Info("Fary", 250)),


        ScrapeProxy("http://682f00ac60f548c0ad400fb44ff4dae550892ee624f:@proxy.scrape.do:8080", Info("seraph_02", 1000)),
        ScrapeProxy("http://scraperapi:258ec9add23194f2f40b3baa8e87bc02@proxy-server.scraperapi.com:8001", Info("seraph_02", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "916b82291490609fc99bad2cc20e3c48030f2889", Info("seraph_02", 250)),


        ScrapeProxy("http://12cb4ffd200e4d3fac86a9a8ece4417ab29f15a4c96:@proxy.scrape.do:8080", Info("seraph_03", 1000)),
        ScrapeProxy("http://scraperapi:472491dd747a979a2c5a9472471b94d7@proxy-server.scraperapi.com:8001", Info("seraph_03", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "cc25609d6daa409b1540c2be2ba34d79a40b8bcf", Info("seraph_03", 250)),


        ScrapeProxy("http://2776bd2636c54cd1a5790e3ba9eff198253379f1877:@proxy.scrape.do:8080", Info("seraph_04", 1000)),
        ScrapeProxy("http://scraperapi:88f6abddcf0345a25a4862ef0c642072@proxy-server.scraperapi.com:8001", Info("seraph_04", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "80e8c372a45b6a28469a94b387839cb916e6dc97", Info("seraph_04", 250)),


        ScrapeProxy("http://2fce8c6503c54fb3a25cf6a8132fbe0391aae51df6e:@proxy.scrape.do:8080", Info("Ivoncita", 1000)),
        ScrapeProxy("http://scraperapi:8f239b99576cd942e34fad0954de10ec@proxy-server.scraperapi.com:8001", Info("Ivoncita", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "065b7425909a8719c840b093ef63e3fb9bc477fd", Info("Ivoncita", 250)),


        ScrapeProxy("http://8c86b1eb192245ccbfe15d5eb2ab73be0de6e0f1e41:@proxy.scrape.do:8080", Info("Ned", 1000)),
        ScrapeProxy("http://scraperapi:7e2cd9f5cd5b7efffab2dadb797a1179@proxy-server.scraperapi.com:8001", Info("Ned", 1000)),
        ScrapeHTTP("https://scrape.serper.dev", "a93545e4a2e0764bebd470adabf446de8f688897", Info("Ned", 250)),


        ScrapeProxy("http://b15a23b80bbf4c30926e645c1d1aa49814ef5e1a58c:@proxy.scrape.do:8080", Info("Keneth", 1000)),
        ScrapeProxy("http://scraperapi:9e4238cdc78d3a0f0ef2002dcf2a7269@proxy-server.scraperapi.com:8001", Info("Keneth", 1000)),

        ScrapeProxy("http://0c7eb7943ebf4e43853b8983218376228dd75e8519f:@proxy.scrape.do:8080", Info("Kumi", 1000)),
        ScrapeProxy("http://scraperapi:2570f81a2a2939e15f28671103541156@proxy-server.scraperapi.com:8001", Info("Kumi", 1000)),


        ScrapeProxy("http://0a53af20d58744cf9991c3b5a3e9e238c89f5a24ea0:@proxy.scrape.do:8080", Info("ROjin", 1000)),
        ScrapeProxy("http://scraperapi:1538a3ab82a29cec49b1109a02692a2a@proxy-server.scraperapi.com:8001", Info("ROjin", 1000)),


        ScrapeProxy("http://d16d04a9b77c4107b6d94198f6c88dc5b3c70bc670c:@proxy.scrape.do:8080", Info("Yunshi", 1000)),
        ScrapeProxy("http://scraperapi:f04aea33ff27753a32ada2e15b562316@proxy-server.scraperapi.com:8001", Info("Yunshi", 1000)),


        ScrapeProxy("http://0c63b40fd3a4488ba7f94b49177ec303ddf1cf06ff1:@proxy.scrape.do:8080", Info("Sidonie", 1000)),
        ScrapeProxy("http://scraperapi:0ba288a83ca960d01b442db1c3b466ad@proxy-server.scraperapi.com:8001", Info("Sidonie", 1000)),

        ScrapeProxy("http://86d155d0107546b09d598e714f3b6a7474a51f5c91a:@proxy.scrape.do:8080", Info("Bayadares", 1000)),
        ScrapeProxy("http://scraperapi:4b25f539218b33ffdba94320432874c5@proxy-server.scraperapi.com:8001", Info("Bayadares", 1000)),


        ScrapeProxy("http://0cf9cd73df29473293383cd0018860aa018abe72c52:@proxy.scrape.do:8080", Info("Lincoln", 1000)),
        ScrapeProxy("http://scraperapi:deb4f5cb9b289c7bb8b9b8ab13ab81ca@proxy-server.scraperapi.com:8001", Info("Lincoln", 1000)),


        ScrapeProxy("http://9343d9750ea84168a4d0bc329a6b027bcaf3bab101a:@proxy.scrape.do:8080", Info("Rivkin", 1000)),
        ScrapeProxy("http://scraperapi:fd47a4bfb978252b1e25abcf867639e8@proxy-server.scraperapi.com:8001", Info("Rivkin", 1000)),
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
