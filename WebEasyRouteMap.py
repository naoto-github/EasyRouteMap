from flask import Flask, render_template, request
import json
from RouteManager import RouteManager
from JTalk import JTalk

JSON_FILE = "json/route.json"
WAV_DIR = "static/sound/"

route = None

app = Flask(__name__)

@app.route("/")
def index():

    with open(JSON_FILE, "r") as f:
        route = json.load(f)
        RouteManager.save(route, JSON_FILE)    
        JTalk.save(route, WAV_DIR)    
        
    template = render_template("template.html", route=route)

    return template

@app.route("/", methods=["POST"])
def post():

    #print(request.json)
    
    # フォームの値を取得
    start_lat = float(request.json["start-lat"])
    start_lng = float(request.json["start-lng"])
    goal_lat = float(request.json["goal-lat"])
    goal_lng = float(request.json["goal-lng"])

    start = {
        "lat": start_lat,
        "lon": start_lng
    }
    
    goal = {
        "lat": goal_lat,
        "lon": goal_lng
    }

    
    # JSONファイルを読込
    if request.method == "POST":
        
        with open(JSON_FILE, "r") as f:
            
            route = RouteManager.request(start, goal)
            RouteManager.save(route, JSON_FILE)
            JTalk.save(route, WAV_DIR)

            return route

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
        
if __name__ == "__main__":
    app.run(debug=True)
    
