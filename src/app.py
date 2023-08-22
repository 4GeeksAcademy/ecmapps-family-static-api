"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

#Get one member
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    print(member)
    if member == False:
        return jsonify("Incorrect id"), 400
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def add_member():
    request_body = request.get_json(force=True)
    member = jackson_family.add_member(request_body)
    if member == False:
        return jsonify("Missing required data fields"), 400
    return jsonify("Success"), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id) == False:
        return jsonify("Incorrect id"), 400
    return jsonify("Deleted member successfully"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
