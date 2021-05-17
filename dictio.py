from data.db import DB
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

swagger.template = {
    "swagger": "2.0",
    "info": {
        "title": "Dictio API",
        "description": "Interactive dictionary API",
        "contact": {
            "responsibleDeveloper": "Jacinto Mba Cantero",
            "email": "jacinto[- at -]gmail.com",
            "url": "jazbelt.net"
        },
        "version": "0.0.1"
    },
    "basepath": "/dictio"
}

MONGO_URL = "mongodb://server"
MONGO_DB = "dictio"

db = DB(MONGO_URL, MONGO_DB)
db.connect()


@app.route("/dictio/alphabet", methods=["GET"])
def getAlphabet():
    """
    This endpoint returns the letters of the alphabet that forms the dictionary
    ---
    definitions:
      Alphabet:
        type: array
        items:
          type: string
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


@app.route("/dictio/<letter>/<word>")
def getWord(letter, word):
    """
    This endpoint returns de definition of a word given its name and initial
    ---
    definitions:
      Word:
        type: string
        example: 
          "Foo"
      Letter:
        type: string
        example:
          "A"
      Definition:
        type: string
        example:
          "Lorem ipsum dolor sit amet"
    parameters:
    - name: letter
      in: path
      required: true
      schema:
        $ref: '#/definitions/Letter'
    - name: word
      in: path
      required: true
      schema:
        $ref: '#/definitions/Word'
    responses:
      200:
        description: Definition of wanted word
        schema:
          $ref: "#/definitions/Definition"
    """
    result = db.find_word(letter, word)
    return {"word": result["word"], "definition": result["definition"]}


app.run(debug=True)