from flask import Flask, render_template, request
import json
from RouteManager import RouteManager
from JTalk import JTalk

JSON_FILE = "json/route.json"
WAV_DIR = "static/sound/"

with open(JSON_FILE, "r") as f:
    route = json.load(f)
    RouteManager.save(route, JSON_FILE)    
    JTalk.save(route, WAV_DIR)    
    audios = JTalk.load(route, WAV_DIR)

    response = {
        "route": route,
        "audios": audios
    }
    
    response_data = json.dumps(response)
    
app = Flask(__name__)

@app.route("/")
def index():
        
    template = render_template("template.html", response=response_data)

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
            route = RouteManager.addSlopeInstruction(route)            
            RouteManager.save(route, JSON_FILE)
            JTalk.save(route, WAV_DIR)
            audios = JTalk.load(route, WAV_DIR)

            response = {
                "route": route,
                "audios": audios
            }

            response_data = json.dumps(response)
            
            return response_data

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
        
if __name__ == "__main__":
    app.run(debug=True)
    
