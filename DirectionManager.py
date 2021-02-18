from urllib.request import Request, urlopen
import json

# 出力ファイル
OUTPUT_PATH = "./json/route.json"

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

# MapBox API
base_url = "https://api.mapbox.com/directions/v5/mapbox/walking/"
access_token = "pk.eyJ1IjoibmFvdG8tbWFwYm94IiwiYSI6ImNrZHkybTg2NDJzM2EydG9kMGQ1ZGhsbmUifQ.e0EC_EqmUkQgUG_JWBwT_g"
steps = "true"
language = "ja"
url = f"{base_url}{start['lon']},{start['lat']};{goal['lon']},{goal['lat']}/?access_token={access_token}&steps={steps}&language={language}"
#print(url)

# MapBoxAPIへアクセス
request = Request(url)
response = urlopen(request)
data = response.read()
directions = json.loads(data)

# Leg Object
leg_distance = directions["routes"][0]["legs"][0]["distance"]
leg_duration = directions["routes"][0]["legs"][0]["duration"]
steps = directions["routes"][0]["legs"][0]["steps"]
#print(f"leg_distance={leg_distance}")    
#print(f"leg_duration={leg_duration}")

# Step Object
step_list = []
for step in steps:
    
    step_distance = step["distance"]
    step_duration = step["duration"]
    maneuver = step["maneuver"]        
    intersections = step["intersections"]    
    
    #print(f"step_distance={step_distance}")    
    #print(f"step_duration={step_duration}")

    # Maneuver Object
    maneuver_type = maneuver["type"]
    maneuver_instruction = maneuver["instruction"]

    #print(f"maneuver_type={maneuver_type}")    
    #print(f"maneuver_instruction={maneuver_instruction}")    
    
    # Intersection Object
    location_list = []
    for intersection in intersections:
        location = intersection["location"]
        #print(f"{location[1]},{location[0]}")
        location_dict = {
            "lat": location[1],
            "lon": location[0]
        }
        location_list.append(location_dict)


    step_dict = {
        "distance": step_distance,
        "duration": step_duration,
        "type": maneuver_type,
        "instruction": maneuver_instruction,
        "locations": location_list
    }

    step_list.append(step_dict)
        

route_dict = {
    "start":{
        "lat": start["lat"],
        "lon": start["lon"],
    },
    "goal":{
        "lat": goal["lat"],
        "lon": goal["lon"],
    },
    "distance": leg_distance,
    "duration": leg_duration,    
    "steps": step_list
}

#print(json.dumps(route_dict, indent=2, ensure_ascii=False))

with open(OUTPUT_PATH, "w") as f:
    json.dump(route_dict, f, indent=2, ensure_ascii=False)
    print(f"Save as {OUTPUT_PATH}")
