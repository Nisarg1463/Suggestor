from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

apiKey = 'kMl9TQ4wS6S90ElOEWy_rxeaboaf9huxq_sf89uduZg'


@app.route('/locations' , methods=['GET'])
def locations():
    coordinates = request.args['coords'].split()
    radius = int(request.args['r'])
    limit = int(request.args['limit'])
    print(len(coordinates))
    data = requests.get(f'https://api.geoapify.com/v2/places?categories=accommodation,activity,catering,entertainment,heritage,leisure,natural,national_park,rental,tourism,camping,beach,sport&filter=circle:{coordinates[1]},{coordinates[0]},{radius}&limit={limit}&bias=proximity:{coordinates[1]},{coordinates[0]}&apiKey=feeb6e2716d14e1183b5855688fca6fa').json()
    print(data)
    print(f'https://api.geoapify.com/v2/places?categories=catering&filter=circle:{coordinates[1]},{coordinates[0]},{radius}&limit={limit}&apiKey=feeb6e2716d14e1183b5855688fca6fa')
    return data


if __name__ == '__main__':
    app.run(debug=True)
