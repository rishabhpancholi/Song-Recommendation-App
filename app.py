from flask import Flask, render_template, request, jsonify
import joblib 
import pandas as pd
from utils import get_recommendations

app = Flask(__name__)

# Load dataset and similarity matrix
songs_df = pd.read_csv("artifacts/songs_cleaned.csv")  # Load cleaned song data
similarity = joblib.load(open("artifacts/similarity_matrix.pkl", "rb"))  # Load precomputed similarity matrix

@app.route("/")
def index():
    """Render the homepage with top 50 popular songs and genre filters."""
    genres = sorted(songs_df['playlist_genre'].dropna().unique())  # Get unique genres
    songs = songs_df.sort_values(by='track_popularity', ascending=False).head(51).to_dict(orient='records')  # Get top 50 songs

    return render_template('popular.html', songs=songs, genres=genres)

@app.route("/filter_songs", methods=['POST'])
def filter_songs():
    """Filter popular songs based on selected genre."""
    genre = request.json.get('genre', '')

    if genre:
        filtered_songs = songs_df[songs_df['playlist_genre'] == genre].sort_values(by='track_popularity', ascending=False).head(51)
    else:
        filtered_songs = songs_df.sort_values(by='track_popularity', ascending=False).head(51)

    return jsonify(filtered_songs.to_dict(orient='records'))

@app.route("/recommendation")
def recommend():
    """Render the song recommendation page with filter options."""
    genres = sorted(songs_df['playlist_genre'].dropna().unique())  # Get unique genres
    songs = songs_df.to_dict(orient='records')  # Convert songs data to dictionary format

    return render_template('recommendation.html', genres=genres, songs=songs)

@app.route("/filter_songs_recommend", methods=['POST'])
def filter_songs_recommend():
    """Filter songs based on selected genre for recommendation."""
    genre = request.json.get('genre', '')

    if genre:
        filtered_songs = songs_df[songs_df['playlist_genre'] == genre]
    else:
        filtered_songs = songs_df

    return jsonify(filtered_songs.to_dict(orient='records'))    

@app.route("/get_recommendations", methods=['POST'])
def fetch_recommendations():
    """Fetch song recommendations based on a given song name."""
    song_name = request.json.get('song', '')  # Get user-selected song name
    recommendations = get_recommendations(song_name, songs_df, similarity)  # Get recommendations

    return jsonify(recommendations)

# Define mood clusters and their corresponding indices in the dataset
mood_clusters = {
    "Energetic": 0,
    "Groovy": 1,
    "Sad": 2,
    "Calm": 3,
    "Happy": 4
}

@app.route("/mood")
def mood_based_recommendation():
    """Render the mood-based recommendation page."""
    songs = songs_df.to_dict(orient='records')

    return render_template('mood.html', moods=mood_clusters.keys(), songs=songs)

@app.route("/filter_songs_mood", methods=['POST'])
def filter_songs_mood():
    """Filter songs based on mood and return the top 50 sorted accordingly."""
    mood = request.json.get('mood', '')
    cluster = mood_clusters.get(mood)  # Get cluster index for selected mood

    # Define sorting parameters based on mood type
    sort_parameters = {
        "Energetic": ("energy", False),
        "Groovy": ("danceability", False),
        "Sad": ("valence", True),
        "Calm": ("acousticness", False),
        "Happy": ("valence", False)
    }

    if mood in sort_parameters:
        sort_by, ascending = sort_parameters[mood]
        filtered_songs = songs_df[songs_df['cluster'] == cluster].sort_values(by=sort_by, ascending=ascending).head(51)
    else:
        filtered_songs = songs_df.sort_values(by='track_popularity', ascending=False).head(51)

    return jsonify(filtered_songs.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Run the Flask app on port 5001









