from flask import Flask, request, jsonify
from parser import find_locations

app = Flask(__name__)

@app.route("/", methods=["POST"])
def search_locations():
    vehicle_requirements = request.get_json()
    # Call your search logic (implement find_locations in parser.py)
    results = find_locations(vehicle_requirements)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
