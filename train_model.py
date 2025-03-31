import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
# import pickle
import joblib
import requests
from concurrent.futures import ThreadPoolExecutor

#satellite API
satellite_data = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
#Fetch satellite data
def fetch_satellite_data_batch(coords):
    results = {}
    for coord in coords:
        longitude, latitude = coord
        params = {'longitude': longitude, 'latitude': latitude}
        response = requests.get(satellite_data, params=params)
        if response.status_code == 200:
            results[coord] = response.json().get('magnitude',None)
        else:
            results[coord] = None
    return results

def fetch_satellite_data_parallel(data, batch_size=10):
    coords = list(data[['Longitude', 'Latitude']].drop_duplicates().itertuples(index=False, name=None))
    cached_data = {}
    with ThreadPoolExecutor() as executor:
        batches = [coords[i:i + batch_size] for i in range(0, len(coords), batch_size)]
        futures = [executor.submit(fetch_satellite_data_batch, batch) for batch in batches]
        for future in futures:
            cached_data.update(future.result())
        
    data['satellite_data'] = data.apply(
        lambda row: cached_data.get((row['Longitude'], row['Latitude']), None), axis=1
    )
    return data

#Load dataset
try:
    data = pd.read_csv("database.csv")
except FileNotFoundError:
    print("Error: database.csv not found!")
    exit()

required_columns = {'Longitude', 'Latitude', 'Depth', 'Magnitude'}
if not required_columns.issubset(data.columns):
    print(f"Error: Missing one or more required columns: {required_columns - set(data.columns)}")
    exit()

print("Fetching satellite data....")
data = fetch_satellite_data_parallel(data)
print("Satellite data fetched successfully.")

# data['satellite_data'] = data.apply(
#     lambda row: fetch_satellite_data(row['Longitude'], row['Latitude']), axis=1
# )

if 'satellite_data' not in data.columns:
    raise ValueError("Satellite data column not found. Ensure satellite data is correctly fetched.")

# data.dropna(inplace=True)
data['satellite_data'].fillna(data['satellite_data'].median(), inplace=True)

if data.shape[0] == 0:
    raise ValueError("Dataset is empty after cleaning. Please check the input data and satellite API.")


X = data[['Latitude', 'Longitude', 'Depth','satellite_data']] #features
y = data['Magnitude'] #target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, 'earthquake_model.joblib')
