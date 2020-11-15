from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        "name": "Andy's Store",
        "items": [
            {"name": "Item 1", "price": 15.99}
        ]
    }
]


# POST /store/ data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>/
@app.route('/store/<string:name>')
def get_store(name):
    pass


# GET /store/
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/ data: {name:, price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass


# GET /store/<string:name>/item/
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    pass


app.run(port=5000)
