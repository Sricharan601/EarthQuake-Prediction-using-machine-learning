from flask import Blueprint, render_template, request , jsonify , redirect, url_for
from .api import get_satellite_data
import joblib
import pandas as pd
# from .api import get_satellite_data, get_iot_data
from .model import predict_earthquake


main = Blueprint('main', __name__)

# Load the trained model
model = joblib.load('earthquake_model.joblib')

@main.route('/')
def index():
    return render_template('index1.html')

@main.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        depth = float(request.form['depth'])

        # Fetch satellite data
        satellite_data = get_satellite_data(longitude, latitude)

        # Prepare input for prediction
        features = pd.DataFrame([[latitude, longitude, depth, satellite_data]],
                                 columns=['Latitude', 'Longitude', 'Depth', 'satellite_data'])

        # Predict using the model
        prediction = model.predict(features)[0]

        return render_template('result1.html', prediction=round(prediction, 2))
    except Exception as e:
        return f"An error occurred: {e}", 400



#backup-code:
# def init_routes(app):
#     @app.route('/')
#     def index():
#         return render_template('index1.html')    
#     @app.route('/predict', methods=['POST','GET'])
#     def predict():
#         try:
            
#             longitude = float(request.form['longitude'])
#             latitude = float(request.form['latitude'])
#             depth = float(request.form['depth'])

#             satellite_data = get_satellite_data()
#             # iot_data = get_iot_data()

#             input_data = pd.DataFrame([{
#                 'longitude': longitude,
#                 'latitude' : latitude,
#                 'depth' : depth,
#                 'satellite_data' : satellite_data['magnitude'],
#                 # 'iot_data' : iot_data
#             }])

#             prediction = predict_earthquake(longitude, latitude, depth, satellite_data['magnitude'])
#             # prediction = predict_earthquake(longitude, latitude, depth, satellite_data['magnitude'], iot_data)
#             return render_template(
#                 'result1.html',
#                 prediction=prediction,
#                 longitude=longitude,
#                 latitude=latitude,
#                 depth=depth,
#                 satellite_data=satellite_data,
#                 # iot_data=iot_data
#             )
#         except Exception as e:
#             return render_template('result1.html', prediction=f"Error: {e}")
#         # return jsonify({'prediction': prediction})
#         #return render_template('result.html', prediction_text=prediction)