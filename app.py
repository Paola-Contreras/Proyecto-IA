from surprise.model_selection import train_test_split
from surprise import Dataset, Reader, SVD
from flask import Flask, render_template
import random as rand
import pandas as pd
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
ratings_df = pd.read_csv('./data/ratings.csv', low_memory=False)
movies_metadata_df = pd.read_csv('./data/movies_metadata.csv', low_memory=False)

reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.2)

algo = SVD()
algo.fit(trainset)

def get_recommendations(user_id):
    unrated_items = [item_id for item_id in ratings_df['movieId'].unique() if not trainset.knows_item(item_id) and trainset.knows_user(user_id)]
    
    predictions = []
    for item_id in unrated_items:
        predicted_rating = algo.predict(user_id, item_id).est
        predictions.append(predicted_rating)
    
    recommendations = pd.DataFrame({'movieId': unrated_items, 'predicted_rating': predictions})
    recommendations_with_metadata = pd.merge(recommendations, movies_metadata_df[['id', 'title', 'poster_path']], left_on='movieId', right_on='id', how='left')
    recommendations_with_metadata = recommendations_with_metadata.dropna(subset=['title'])
    top_recommendations = recommendations_with_metadata.sort_values('predicted_rating', ascending=False)
    return top_recommendations

def shuffleUser():
    user_id = rand.randint(1, 300)
    return user_id

def randomUserRecos():
    user_id = shuffleUser()
    recommendations = get_recommendations(user_id)
    return recommendations


@app.route("/")
def index():
    
    movies = randomUserRecos()

    # Info
    movies = movies.head(5)
    titles = list((movies['title']))
    posters = list((movies['poster_path']))
    posters_link = []
    [posters_link.append('https://image.tmdb.org/t/p/original' + i) for i in posters]
    # title = 'Avatar 2'
    # image_url = "https://lumiere-a.akamaihd.net/v1/images/e9fa83c7242fb46fa962150a60301d4e_2764x4096_7a402a9f.jpeg?region=0,0,2764,4096"
    return render_template('index.html', title = titles, image_url=posters_link)

