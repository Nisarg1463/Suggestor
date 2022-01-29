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
    # 'https://discover.search.hereapi.com/v1/discover?at=52.5228,13.4124&q=petrol+station&limit=5&apiKey=kMl9TQ4wS6S90ElOEWy_rxeaboaf9huxq_sf89uduZg'

    data = requests.get(
        f'https://browse.search.hereapi.com/v1/browse?at={coordinates[0]},{coordinates[1]}&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}&limit={limit}'
    ).json()
    return data


if __name__ == '__main__':
    app.run(debug=True)
