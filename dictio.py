from config.config import Config
from data.db import DB
from flask import Flask, jsonify, abort
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

cfg = Config()
db = DB(cfg.mongo_url, cfg.mongo_db)
db.connect()


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/dictio/alphabet", methods=["GET"])
def get_alphabet():
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
def get_word(letter, word):
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
        type: object
        properties:
          word:
            type: string
          definition:
            type: string
          example:
            word: foo
            definition: Lorem ipsum dolor sit amet
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
    if result is None:
        abort(404, "Word not found")
    return result


@app.route("/dictio/<letter>/random")
def get_random_word(letter):
    """
    This endpoint returns a random word starting with given letter
    ---
    parameters:
      - name: letter
        in: path
        required: true
        schema:
          $ref: '#/definitions/Letter'
    responses:
      200:
        description: Definition of the random word
        schema:
          $ref: '#/definitions/Definition'
    """
    result = db.find_random_word(letter.lower())
    if result is None or len(result) == 0:
        abort(404, "Letter not found")
    return result[0]


@app.route("/dictio/random")
def get_random_dictionary():
    """
    This endpoint returns a dictionary with one random word per letter
    ---
    definitions:
      Dictionary:
        type: object
        additionalProperties:
          $ref: '#/definitions/Definition'
    responses:
      200:
        description: Random dictionary
        schema:
          $ref: '#/definitions/Dictionary'
    """
    result = db.find_random_dictionary()
    if result is None or len(result) == 0:
        abort(404, "Letter not found")
    return result


app.run(debug=cfg.debug, host="0.0.0.0")