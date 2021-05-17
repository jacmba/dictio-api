from data.db import DB
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

MONGO_URL = "mongodb://server"
MONGO_DB = "dictio"

db = DB(MONGO_URL, MONGO_DB)
db.connect()


@app.route("/dictio/alphabet")
def main():
    """
    This endpoint returns the letters of the alphabet that forms the dictionary
    ---
    definitions:
      Alphabet:
        type: array
        items: string
        example:
          ["A", "B", "C"]
    responses:
      200:
        description: Array of letters
        schema:
          $ref: '#/definitions/Alphabet'
    """
    alphabet = db.find_alphabet()
    return jsonify(alphabet)


app.run(debug=True)