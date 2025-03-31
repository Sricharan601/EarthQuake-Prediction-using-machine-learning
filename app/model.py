import joblib
import numpy as np
import pandas as pd

model = joblib.load("earthquake_model.joblib")
# def predict_earthquake(longitude, latitude, depth, satellite_data, iot_data)
def predict_earthquake(longitude, latitude, depth, satellite_data):
    input_data = np.array([longitude, latitude, depth, satellite_data]).reshape(1, -1)
    prediction = model.predict(input_data)[0]
    return prediction