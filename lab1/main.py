import string
import json
from flask import Flask, request, jsonify
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345678",
    host="34.44.45.60",
    port="5432"
)

cur = conn.cursor()

app = Flask(__name__) # setup initial flask app; gets called throughout in routes

@app.route('/') #python decorator 
def hello_world(): #function that app.route decorator references
  response = 'Ben is the KING'
  return response


@app.route("/get_polygon")
def get_polygon():
    return jsonify(get_geojson())
    
def get_geojson():
    cur.execute("""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(geom)::json,
                    'properties', json_build_object('id', id)
                )
            )
        )
        FROM geometries;
    """)
   
    geojson = cur.fetchone()[0] 
    # cur.close()
    # conn.close()
    return geojson

if __name__ == "__main__":
    app.run(
      #debug=True, #shows errors 
      host='0.0.0.0', #tells app to run exposed to outside world
      port=5000)
