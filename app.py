from pprint import pprint
from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

apiKey = "kMl9TQ4wS6S90ElOEWy_rxeaboaf9huxq_sf89uduZg"


@app.route("/locations", methods=["GET"])
def locations():
    coordinates = request.args["coords"].split()
    radius = int(request.args["r"])
    limit = int(request.args["limit"])
    limit = int(limit/4)
    data = {}
    data['restaurants'] = requests.get(
        f"https://discover.search.hereapi.com/v1/discover?limit={limit}&q=restaurant&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}"
    ).json()
    
    data['malls'] = requests.get(
        f"https://discover.search.hereapi.com/v1/discover?limit={limit}&q=mall&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}"
    ).json()

    data['tourism'] = requests.get(
        f"https://discover.search.hereapi.com/v1/discover?limit={limit}&q=tourism&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}"
    ).json()

    data['entertainment'] = requests.get(
        f"https://discover.search.hereapi.com/v1/discover?limit={limit}&q=entertainment&apiKey={apiKey}&in=circle:{coordinates[0]},{coordinates[1]};r={radius}"
    ).json()
    
    # pprint(data)
    # print(len(data['items']))
    # data = requests.get(
    #     f"https://api.geoapify.com/v2/places?categories=accommodation,activity,catering,entertainment,heritage,leisure,natural,national_park,rental,tourism,camping,beach,sport&filter=circle:{coordinates[1]},{coordinates[0]},{radius}&limit={limit}&bias=proximity:{coordinates[1]},{coordinates[0]}&apiKey=feeb6e2716d14e1183b5855688fca6fa"
    # ).json()
    # print(
    #     f"https://api.geoapify.com/v2/places?categories=catering&filter=circle:{coordinates[1]},{coordinates[0]},{radius}&limit={limit}&apiKey=feeb6e2716d14e1183b5855688fca6fa"
    # )
    return data


if __name__ == "__main__":
    app.run(debug=True)
