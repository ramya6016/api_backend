import math
import numpy as np
#y simple Flask Hello World app for you to get started with...
from flask import Flask, request, jsonify
from flask import Flask
import firebase_admin
from flask_cors import CORS, cross_origin
from firebase_admin import firestore
from firebase_admin import credentials
cred = credentials.Certificate("/home/teamelitegameez/mysite/gameez-e202a-firebase-adminsdk-87j7e-d16deef713.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = firebase_admin.firestore.client()
def calc(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert latitude and longitude from degrees to radians
    if(lat1 is None or lon1 is None or lat2 is None or lon2 is None):
        return -1
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula to calculate distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * a*np.arctan2(math.sqrt(a), math.sqrt(1 - a))
    radius_of_earth = 6371  # Earth's radius in kilometers
    distance = radius_of_earth * c
    return distance
@app.route('/')
def hello_world():
    return 'Hello from Flask!'
@app.route('/signup',methods=["POST"])
def signup():
    try:
        # Get data from the request
        data = request.json
        # Add data to Firestore
        doc_ref = db.collection('userdb').add(data)
        return jsonify({"message": "Data added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/match', methods=["POST"])
def match():
  data=request.json
  latitude=data.get('latitude')
  longitude=data.get('longitude')
  radius=data.get('radius')
  docs_ref = db.collection("userdb").stream()
  for doc in docs_ref:
      json1= doc.to_dict()
      lat=json1.get('Latitude')
      lon=json1.get('Longitude')
      distance=calc(lat,lon,latitude,longitude)
      if(distance is None):
          continue
      result={}
      if(distance<=radius  and json1 is not None):
        result['userid']=json1.get('userid')
        result['username']=json1.get('name')
        result['lat']= json1.get('Latitude')
        result['lon'] = json1.get('Longitude')
  return result






if __name__ == '__main__':
    app.run()
