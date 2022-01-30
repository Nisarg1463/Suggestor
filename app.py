from pprint import pprint
from flask import Flask, request, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, db
from cryptography.fernet import Fernet

app = Flask(__name__)

apiKey = 'here_api_key'

cred = credentials.Certificate('serviceKey.json')
default_app = firebase_admin.initialize_app(
    cred,
    {
        'databaseURL': 'Your_database_url'
    },
)


@app.route('/locations', methods=['GET'])
def locations():
    coordinates = request.args['coords'].split()
    radius = int(request.args['r'])
    limit = int(request.args['limit'])
    limit = int(limit / 4)
    data = {}
    data['restaurants'] = requests.get(
        f'https://discover.search.hereapi.com/v1/discover?limit={limit}&q=restaurant&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}'
    ).json()

    data['malls'] = requests.get(
        f'https://discover.search.hereapi.com/v1/discover?limit={limit}&q=mall&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}'
    ).json()

    data['tourism'] = requests.get(
        f'https://discover.search.hereapi.com/v1/discover?limit={limit}&q=tourism&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}'
    ).json()

    data['entertainment'] = requests.get(
        f'https://discover.search.hereapi.com/v1/discover?limit={limit}&q=entertainment&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}'
    ).json()

    # pprint(data)
    # print(len(data['items']))
    # data = requests.get(
    #     f'https://api.geoapify.com/v2/places?categories=accommodation,activity,catering,entertainment,heritage,leisure,natural,national_park,rental,tourism,camping,beach,sport&filter=circle:{coordinates[1]},{coordinates[0]},{radius}&limit={limit}&bias=proximity:{coordinates[1]},{coordinates[0]}&apiKey=feeb6e2716d14e1183b5855688fca6fa'
    # ).json()
    # print(
    #     f'https://api.geoapify.com/v2/places?categories=catering&filter=circle:{coordinates[1]},{coordinates[0]},{radius}&limit={limit}&apiKey=geoapify_key'
    # )
    return data


@app.route('/findPlace', methods=['GET'])
def findPlace():
    coordinates = request.args['coords'].split()
    radius = int(request.args['r'])
    limit = int(request.args['limit'])
    query = request.args['query']
    data = requests.get(
        f'https://discover.search.hereapi.com/v1/discover?limit={limit}&q={query}&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}'
    ).json()
    return data


@app.route('/register', methods=['GET'])
def register():
    key = Fernet.generate_key()
    fernet = Fernet(key)
    print(key)
    email = request.args['email']
    username = request.args['username']
    password = request.args['password']
    encryption = fernet.encrypt(password.encode())
    encryption = key + encryption
    print(encryption)
    ref = db.reference('/users')
    if ref.get() == None:
        structure = {'password': encryption.decode(), 'email': email}
        ref.set({username: structure})
    else:
        data = ref.get()
        if username not in data.keys():
            structure = {'password': encryption.decode(), 'email': email}
            data[username] = structure
            ref.update(data)
        else:
            return jsonify('user found')
    return jsonify('success')


@app.route('/retrive', methods=['GET'])
def retrive():
    ref = db.reference('/users')
    data = ref.get()
    for key in data.keys():
        encoded = data[key]['password'].encode()
        fernet_key = encoded[:44]
        fernet = Fernet(fernet_key)
        data[key]['password'] = fernet.decrypt(encoded[44:]).decode()

    return data


@app.route('/login')
def login():
    data = retrive()
    username = request.args['username']
    password = request.args['password']
    found = False
    for key in data:
        if key == username:
            if password == data[key]['password']:
                found = True
    return jsonify(found)


if __name__ == '__main__':
    app.run(debug=True)
