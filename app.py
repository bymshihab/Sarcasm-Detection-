`   import json
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sqlite3

app = Flask(__name__)
DATABASE = "reviews.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review TEXT
        )
        """
    )
    conn.commit()
    conn.close()

initialize_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    sentences = data["sentences"]

    # Load the tokenizer and model
    tokenizer_path = "tokenizer.json"
    model_path = "model.h5"

    with open(tokenizer_path, "r") as json_file:
        tokenizer_json = json_file.read()
        tokenizer = keras.preprocessing.text.tokenizer_from_json(tokenizer_json)

    model = tf.keras.models.load_model(model_path)

    # Tokenize and pad the input sentences
    sequences = tokenizer.texts_to_sequences(sentences)
    padded_sequences = pad_sequences(sequences, maxlen=100, padding="post", truncating="post")

    # Make predictions
    predictions = model.predict(padded_sequences)

    # Format the predictions as a JSON response
    response = {"predictions": predictions.tolist()}
    return jsonify(response)

@app.route("/review", methods=["POST"])
def add_review():
    data = request.get_json()
    review = data["review"]

    # Insert the review into the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO reviews (review) VALUES (?)", (review,))
    conn.commit()
    conn.close()

    # Return a success response
    response = {"message": "Review added successfully"}
    return jsonify(response)

if __name__ == "__main__":
    app.run()
