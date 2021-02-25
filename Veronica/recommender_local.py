"""d.	recommender.py runs the ML model to select the next pet to display
i.	Import CountVectorizer, PyMongo, Pandas, jsonUtil, and Numpy modules
ii.	Declare arrays to hold pets in different categories
1.	not_shown_yet_array = []
2.	shown_array = [] is an array containing two arrays
a.	voted_up = []
b.	voted_down = []
iii.	Declare update_buckets() function
1.	Get latest user choice
2.	Move pet from 
iv.	Declare get_recommendations() function
def get_recommendations(pet_id, cosine_sim):
	# Get the index of the pet that matches the pet_id
	idx = indices[pet_id]
	# Get the pairwise similarity scores
	sim_scores = list(enumerate(cosine_sim[idx]))
	# Sort the pets based on their similarity scores
	sim_scores = sorted(sim_scores, key=lambda x: x[1], 
reverse = True)
# Get the ID of the top-matching pet
sim_scores = sim_scores[1]
next_pet_index = sim_scores[0]
return metadata[‘pet_id’].iloc[next_pet_index]
v.	Run get_recommendations() function
"""