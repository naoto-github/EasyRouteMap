from urllib.request import Request, urlopen
import json

class ElevationManager:

    # 標高APIへアクセス
    @classmethod
    def request(self, lat, lon):
        url = f"https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php?lon={lon}&lat={lat}&outtype=JSON"

        request = Request(url)
        response = urlopen(request)
        data = response.read()
        data_json = json.loads(data)

        elevation = float(data_json["elevation"])
        
        return elevation
