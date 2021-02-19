from urllib.request import Request, urlopen
import json
from ElevationManager import ElevationManager

class RouteManager:

    # MapBox APIへアクセス
    @classmethod
    def request(self, start, goal):

        base_url = "https://api.mapbox.com/directions/v5/mapbox/walking/"
        access_token = "pk.eyJ1IjoibmFvdG8tbWFwYm94IiwiYSI6ImNrZHkybTg2NDJzM2EydG9kMGQ1ZGhsbmUifQ.e0EC_EqmUkQgUG_JWBwT_g"
        steps = "true"
        language = "ja"
        
        url = f"{base_url}{start['lon']},{start['lat']};{goal['lon']},{goal['lat']}/?access_token={access_token}&steps={steps}&language={language}"

        # MapBoxAPIへアクセス
        request = Request(url)
        response = urlopen(request)
        data = response.read()
        directions = json.loads(data)

        # 変換
        route = self._convert(start, goal, directions)

        return route

    # シンプルなJSON形式に変換
    def _convert(start, goal, directions):
        
        # Leg Object
        leg_distance = directions["routes"][0]["legs"][0]["distance"]
        leg_duration = directions["routes"][0]["legs"][0]["duration"]
        steps = directions["routes"][0]["legs"][0]["steps"]
        #print(f"leg_distance={leg_distance}")    
        #print(f"leg_duration={leg_duration}")

        # Step Object
        step_list = []
        for i, step in enumerate(steps):
            
            step_distance = step["distance"]
            step_duration = step["duration"]
            maneuver = step["maneuver"]        
            intersections = step["intersections"]
            sound = "sound_" + str(i).zfill(2) + ".wav"
        
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
                
                latitude = location[1]
                longitude = location[0]                
                
                elevation = ElevationManager.request(latitude, longitude)
                
                location_dict = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "elevation": elevation
                }
                location_list.append(location_dict)


            step_dict = {
                "distance": step_distance,
                "duration": step_duration,
                "type": maneuver_type,
                "instruction": maneuver_instruction,
                "sound": sound,
                "locations": location_list
            }

            step_list.append(step_dict)

        # スタートの標高
        start_elevation = ElevationManager.request(start["lat"], start["lon"])

        # ゴールの標高
        goal_elevation = ElevationManager.request(goal["lat"], goal["lon"])            

        route = {
            "start":{
                "latitude": start["lat"],
                "longitude": start["lon"],
                "elevation": start_elevation
            },
            "goal":{
                "latitude": goal["lat"],
                "longitude": goal["lon"],
                "elevation": goal_elevation                
            },
            "distance": leg_distance,
            "duration": leg_duration,    
            "steps": step_list
        }

        return route

    @classmethod
    def save(self, route, path):
        with open(path, "w") as f:
            json.dump(route, f, indent=2, ensure_ascii=False)
            print(f"Save as {path}")
