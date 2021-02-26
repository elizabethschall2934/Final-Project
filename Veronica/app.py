# Import dependencies
from flask import Flask, render_template
import json
from bson import json_util
import pandas as pd
from numpy import genfromtxt

app = Flask(__name__)

# Read in pet attributes, pet index look-up table, and cosine similarity matrix
pet_attributes_df = pd.read_csv("data/pet_attributes.csv") # Read into Pandas DataFrame
indices_df = pd.read_csv("data/indices.csv") # Read into Pandas DataFrame
cosine_similarity_matrix = genfromtxt("data/cosine_similarity.csv", delimiter=",") # Read into numpy.ndarray

# Convert indices to a pandas series.
indices_ser = pd.Series(indices_df.index, index=indices_df['ID']).drop_duplicates()
    
# - - - Routes - - - 

# Route to render web page
@app.route("/")
def index():
    return render_template("recommender.html")

# API route that accepts the last pet voted and which direction it was voted as arguments
# and decides which pet to display next based on cosine similarity
@app.route("/getNextPet")
def getNextPet():
    # Get index of pet_just_voted
    idx = indices_ser[pet_just_voted]

    # Look up similarity scores between pet_just_voted and every other pet
    sim_scores = list(enumerate(cosine_similarity_matrix[idx]))

    # If the last pet was voted up, sort the similarity scores descending so the closest matches
    # rise to the top. If the last pet was voted down, sort descending instead so that the next pet
    # shown will be as different as possible from the pet that was voted down.
    if up_or_down == "up":
        sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True)
    else:
        sim_scores = sorted(sim_scores, key = lambda x: x[1])

    # Get the pet from the top of the score list.
    next_sim_score = sim_scores[1]

    # Get the index of the pet
    pet_index = next_sim_score[0]

    # Get the ID of the pet. This pet will be displayed next.
    pet_id = pet_attributes_df['ID'].iloc[pet_index]

    # Look up the attributes of the next pet to display.
    next_photo = pet_attributes_df['Photo'].iloc[pet_index]
    next_name = pet_attributes_df['Name'].iloc[pet_index]
    next_species = pet_attributes_df['Species'].iloc[pet_index]
    next_breed = pet_attributes_df['Breed'].iloc[pet_index]
    next_size = pet_attributes_df['Size'].iloc[pet_index]
    next_age = pet_attributes_df['Age'].iloc[pet_index]
    next_color = pet_attributes_df['Color'].iloc[pet_index]

    # Return dictionary containing attributes of next pet
    
if __name__ == "__main__":
    app.run(debug=True)
