from urllib.request import Request, urlopen
import json
from RouteManager import RouteManager
from JTalk import JTalk

# 出力ファイル(JSON)
OUTPUT_JSON_FILE = "./json/route.json"

# 出力ファイル(TEXT)
OUTPUT_TEXT_FILE = "./text/instruction.txt"

# 出力フォルダ(WAV)
OUTPUT_WAV_DIR = "./static/sound/"

# 椙山女学園大学
start = {
    "lat": 35.159419502445,
    "lon": 136.9875941894
}

# 星ヶ丘駅
goal = {
    "lat": 35.1624295,
    "lon": 136.9851778
}

# Mapbox APIで経路取得
route = RouteManager.request(start, goal)

# 勾配情報で更新
route = RouteManager.addSlopeInstruction(route)

# JSONを保存
RouteManager.save(route, OUTPUT_JSON_FILE)

# WAVを保存
JTalk.save(route, OUTPUT_WAV_DIR)

