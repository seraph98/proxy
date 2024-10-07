# api.py
from flask import Flask, jsonify, request
import json
import os
from flask_caching import Cache

app = Flask(__name__)

# 配置缓存
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 900})  # 设置 15 分钟的缓存（900 秒）

@cache.memoize()  # 对这个函数的返回值进行缓存
def load_data_from_file(page):
    file_path = f"data/page_{page}.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    return None

@app.route('/api/p1/solana/pools', methods=['GET'])
def get_data():
    # 从查询参数获取页码
    page = request.args.get('page', default=1, type=int)
    
    # 尝试从缓存加载数据
    data = load_data_from_file(page)
    
    if data is not None:
        return jsonify(data)  # 返回 JSON 格式数据
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    print("Starting the Flask API on port 5000...")
    app.run(host='0.0.0.0', port=5000)  # 在5000端口启动Flask服务
