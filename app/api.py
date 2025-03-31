import requests


SATELLITE_API_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query'

def get_satellite_data(longitude, latitude):
    params = {'longitude': longitude, 'latitude': latitude}
    try:
        response = requests.get(SATELLITE_API_URL, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get('magnitude', 0)  # Default to 0 if not found
        else:
            return 0  # Default to 0 for failed requests
    except Exception:
        return 0 
    






# def get_satellite_data(min_magnitude=4.0, start_time="1980-01-01", end_time="2024-12-31"):
#     # response = requests.get("")
#     # return response.json().get('')
#     url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
#     params = {
#         "format" : "geojson",
#         "starttime":start_time,
#         "endtime":end_time,
#         "minmagnitude": min_magnitude,
#         "orderby": "time"
#     }
#     try: 
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         if data["features"]:
#             event = data["features"][0]["properties"]
#             return {
#                 "magnitude": event["mag"],
#                 "place": event["place"],
#                 "time": event["time"]
#             }
#         else:
#             return{"error":"No data found for the given parameters."}
#     except requests.exceptions.RequestException as e:
#         return {"error": f"API request failed: {e}"}
#def get_iot_data():
# write the iot integration data