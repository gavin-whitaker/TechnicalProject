from flask import Flask, request, jsonify
import json
from math import inf
import os
from parser import parse_json
app = Flask(__name__)
with open('listings.json', 'r') as f:
    data = json.load(f)
print(len(parse_json("listings.json")))
