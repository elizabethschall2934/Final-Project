# Import dependencies
from flask import Flask, render_template
import json
from bson import json_util

app = Flask(__name__)

# Route to render web page
@app.route("/")
def index():
    return render_template("recommender_local.html")

# Route to run recommender_local.py to get next recommended pet based on current voted pet
@app.route("/getNextPet")
def getNextPet(currentPetID):
    # Call recommender_local.py or paste the script here
    # Return json string containing attributes of next pet
    return nextPetAttributes

if __name__ == "__main__":
    app.run(debug=True)
