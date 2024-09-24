from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)

# Load your dataset and preprocess it here (the same steps you did before)
data = pd.read_csv(r'C:\Users\VSS\Desktop\ML projects\Dataset.csv')

# Fill missing cuisines
data['Cuisines'].fillna('Unknown', inplace=True)

# Label encoding for categorical columns
label_encoder = LabelEncoder()
categorical_columns = ['Has Table booking', 'Has Online delivery', 'Is delivering now', 'Switch to order menu']
for col in categorical_columns:
    data[col] = label_encoder.fit_transform(data[col])

# TF-IDF for cuisines
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
cuisines_matrix = tfidf_vectorizer.fit_transform(data['Cuisines'])

# Normalize 'Average Cost for two' and 'Price range'
scaler = StandardScaler()
data[['Average Cost for two', 'Price range']] = scaler.fit_transform(data[['Average Cost for two', 'Price range']])

# Recommendation function
# Update the recommendation function to use 'City' instead of latitude and longitude for location filtering
def recommend_restaurants(user_cuisine=None, user_price_range=None, user_cost=None, user_city=None, num_recommendations=5):
    # Default similarity weights
    weight_cuisine = 1
    weight_price = 1
    weight_cost = 1
    weight_city = 1
    
    # Transform user input into a TF-IDF vector if cuisine is provided
    if user_cuisine:
        user_input = tfidf_vectorizer.transform([user_cuisine])
        cuisine_similarity = cosine_similarity(user_input, cuisines_matrix).flatten()
    else:
        cuisine_similarity = np.ones(len(data))  # Default similarity if no cuisine provided
    
    # Adjust similarity score based on user price range preference if provided
    if user_price_range is not None:
        price_similarity = 1 - abs(data['Price range'] - user_price_range)
    else:
        price_similarity = np.ones(len(data))  # Default similarity if no price range provided
    
    # Adjust similarity score based on user average cost preference if provided
    if user_cost is not None:
        cost_similarity = 1 - abs(data['Average Cost for two'] - user_cost)
    else:
        cost_similarity = np.ones(len(data))  # Default similarity if no cost provided
    
    # Adjust similarity score based on user city if provided
    if user_city:
        city_similarity = data['City'].apply(lambda x: 1 if x.lower() == user_city.lower() else 0)
    else:
        city_similarity = np.ones(len(data))  # Default similarity if no city provided
    
    # Combine all similarities into a final score
    final_similarity = (cuisine_similarity * price_similarity * cost_similarity * city_similarity)
    
    # Normalize final similarity to handle cases with all defaults
    if np.all(final_similarity == 0):
        final_similarity = np.ones(len(data))
    
    # Get the indices of the top similar restaurants
    similar_indices = final_similarity.argsort()[-num_recommendations:][::-1]
    
    # Return the top recommendations
    return data.iloc[similar_indices][['Restaurant Name', 'Cuisines', 'City', 'Price range', 'Average Cost for two', 'Aggregate rating']]
pass


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input from form
    user_cuisine = request.form['cuisine']
    user_price_range = float(request.form['price_range'])
    user_cost = float(request.form['cost'])
    user_city = request.form['city']

    # Call the recommendation function
    recommendations = recommend_restaurants(user_cuisine=user_cuisine, user_price_range=user_price_range, user_cost=user_cost, user_city=user_city)

    # Print recommendations to check if data is correct
    print(recommendations)

    # Return recommendations to the frontend
    return render_template('results.html', recommendations=recommendations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
