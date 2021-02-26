"""c.	recommender_preprocess.py preprocesses the data
i.	Import pet data and convert to json string (or whatever format is needed)
1.	pets = mongo.db.pet_data.find(only first 500 for debugging)
2.	return json_util.dumps(pets)
ii.	Pre-process data in Pandas
2.	Convert NaN’s to ““
3.	Convert to lower case and strip white spaces
iii.	Create metadata soup with createsoup()
iv.	Use CountVectorizer()
v.	Use Scikitlearn cosine_similarity() to compute Cosine similarity scores between each pet and every other pet (could use Manhattan, Euclidean, Pearson
vi.	Use Pickling to store pre-processed data for use by recommender.py
"""

# Import dependencies
from flask import Flask
from flask_pymongo import PyMongo
import json
from bson import json_util
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import savetxt

app = Flask(__name__)

# Use PyMongo to set up mongo connection
app.config["MONGO_URI"] = 'mongodb+srv://TeamCatViz:RockingTeam#1@cluster0.ddihz.mongodb.net/petfinder_db?retryWrites=true&w=majority'
mongo = PyMongo(app)

# Query Mongo db
pets_coll = mongo.db.tx_pet_data.find().limit(50)

# Convert query result to json string
pets_json_string = json_util.dumps(pets_coll)

# Convert json string to Python list of dictionaries
list_of_dictionaries = json.loads(pets_json_string)

print(list_of_dictionaries)

# Declare blank lists to hold pet attributes
id_list = []
names_list = [] # names_list is only used in pet photo captions and is not part of the ML model.
sizes_list = []
species_list = []
breeds_list = []
colors_list = []
ages_list = []
photos_list = []

# Declare a function to check for existence of photos and build photos list
def buildPhotoList(list_of_dictionaries, photos_list):
  # Loop through list of dictionaries to extract photos. If medium-sized photo is present, store its in list.
  # Otherwise store URL to generic paw icon instead.
  for x in range(len(list_of_dictionaries)):
      # Check if a medium photo exists.
      try:
        photo = list_of_dictionaries[x]["photos"][0]
        photos_list.append(photo["medium"])
      except:
          photos_list.append("../static/assets/pawIcon.png")
  return photos_list

# Loop through list of dictionaries to parse out features of interest and store in separate lists
for x in range(len(list_of_dictionaries)):
    id_list.append(list_of_dictionaries[x]["id"])
    names_list.append(list_of_dictionaries[x]["name"])
    sizes_list.append(list_of_dictionaries[x]["size"])
    species_list.append(list_of_dictionaries[x]["species"])
    breeds_list.append(list_of_dictionaries[x]["breeds"]["primary"])
    ages_list.append(list_of_dictionaries[x]["age"])
    # Parse out first color descriptor before adding to colors_list
    color = list_of_dictionaries[x]["colors"]["primary"]
    if bool(color):
        color = color.split()[0]
    colors_list.append(color)

# Call function to build photo URL list
photos_list = buildPhotoList(list_of_dictionaries, photos_list)
    
# Store feature lists in Pandas dataframe
df = pd.DataFrame(list(zip(id_list, names_list, sizes_list, species_list, breeds_list, colors_list, ages_list, photos_list)), columns = ['ID', 'Name', 'Size', 'Species', 'Breed', 'Color', 'Age', 'Photo'])

# Export Pandas dataframe to csv. recommender_local.js will access it to look up the attributes for the next pet to show.
df.to_csv('data/pet_attributes.csv', index=False)

# Drop name column from Pandas dataframe
df.drop('Name', axis=1, inplace=True)
df.drop('Photo', axis=1, inplace=True)

#Replace all NaN values with empty strings
df['ID'] = df['ID'].fillna('')
df['Size'] = df['Size'].fillna('')
df['Species'] = df['Species'].fillna('')
df['Breed'] = df['Breed'].fillna('')
df['Color'] = df['Color'].fillna('')
df['Age'] = df['Age'].fillna('')

# Declare a function to convert all text to lower case and remove spaces
def clean_data(x):
    # Check if the entry is a string or a blank and return appropriately formatted data
    if isinstance(x, str):
        return str.lower(x.replace(" ", ""))
    else:
        return ''

# Apply clean_data function to each dataframe column
df_columns = ['Size', 'Species', 'Breed', 'Color', 'Age']

for column in df_columns:
    df[column] = df[column].apply(clean_data)

# Declare a function to create "metadata soup". Each df row is converted to a string that contains each column value separated by a space, 
# e.g., "small dog pittbullterrier white adult"
def create_soup(x):
    return x['Size'] + ' ' + x['Species'] + ' ' + x['Breed'] + ' ' + x['Color'] + ' ' + x['Age']

# Create a new df column to hold metadata soup
df['MetadataSoup'] = df.apply(create_soup, axis=1)

# Create count matrix (CountVectorizer object)
count = CountVectorizer()

# Fit count matrix to metadata soup
count_matrix = count.fit_transform(df['MetadataSoup'])

# Compute the cosine similarity score between each pet and every other pet.
# The score represents how similar two pets are.
# Pets with similar attributes get a score closer to 1.
# Export cosine_sim (a numpy.ndarray) to csv. Will be called by Flask 'getNextPet' route.
cosine_sim = cosine_similarity(count_matrix, count_matrix)
savetxt('data/cosine_similarity.csv', cosine_sim, delimiter=',')

# Create a look-up table that will be used to retrieve the table index of each pet.
# Drop any duplicated ID's that may exist in dataset.
# Export indices series to csv. Will be called by Flask 'getNextPet' route.
indices = pd.Series(df.index, index=df['ID']).drop_duplicates()
indices.to_csv('data/indices.csv', index=True)



#print(next_pet)

#print(cosine_sim)

#print(count_matrix)

#print(df)
