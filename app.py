# from flask import Flask, render_template, request, jsonify
# from app.routes import init_routes
# import numpy as np
# import pandas as pd
# import joblib
# import requests
from app import create_app


app  = create_app()



if __name__ == '__main__':
    app.run(debug=True)
