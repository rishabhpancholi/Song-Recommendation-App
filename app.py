from flask import Flask,render_template,request,jsonify
import joblib 
import pandas as pd
from utils import get_recommendations

app = Flask(__name__)

# Load dataset and similarity matrix
songs_df = pd.read_csv("artifacts/songs_cleaned.csv")
similarity = joblib.load(open("artifacts/similarity_matrix.pkl", "rb"))


@app.route("/")
def index():
    genres = sorted(songs_df['playlist_genre'].dropna().unique())
    songs = songs_df.sort_values(by='track_popularity',ascending=False).head(51).to_dict(orient='records')

    return render_template('popular.html',songs=songs,genres=genres)


@app.route("/filter_songs",methods=['POST'])
def filter_songs():
    genre = request.json.get('genre','')

    if genre:
       filtered_songs = songs_df[songs_df['playlist_genre']==genre].sort_values(by='track_popularity',ascending = False).head(51)
    else:
       filtered_songs = songs_df.sort_values(by='track_popularity',ascending = False).head(51)

    return jsonify(filtered_songs.to_dict(orient='records'))


@app.route("/recommendation")
def recommend():
     genres = sorted(songs_df['playlist_genre'].dropna().unique())
     songs = songs_df.to_dict(orient='records')

     return render_template('recommendation.html',genres = genres,songs = songs)

@app.route("/filter_songs_recommend",methods=['POST'])
def filter_songs_recommend():
    genre = request.json.get('genre','')

    if genre:
       filtered_songs = songs_df[songs_df['playlist_genre']==genre]
    else:
       filtered_songs = songs_df

    songs_list=[]
    for _, song in filtered_songs.iterrows():
         song_dict = song.to_dict()
         songs_list.append(song_dict)

    return jsonify(filtered_songs.to_dict(orient='records'))    

@app.route("/get_recommendations",methods=['POST'])
def fetch_recommendations():
    song_name = request.json.get('song','')
    
    recommendations = get_recommendations(song_name,songs_df,similarity)
    
    return jsonify(recommendations)


mood_clusters = {
    "Energetic" : 0,
    "Groovy" : 1,
    "Sad" : 2,
    "Calm" : 3,
    "Happy" : 4
}
   
@app.route("/mood")
def mood_based_recommendation():
    songs = songs_df.to_dict(orient='records')

    return render_template('mood.html',moods = mood_clusters.keys(),songs = songs)

@app.route("/filter_songs_mood",methods=['POST'])
def filter_songs_mood():
    mood = request.json.get('mood','')
    cluster = mood_clusters.get(mood)

    sort_parameters = {
        "Energetic" : ("energy",False),
        "Groovy" : ("danceability",False),
        "Sad" : ("valence",True),
        "Calm" : ("acousticness",False),
        "Happy" : ("valence",False)
    }

    if mood in sort_parameters:
       sort_by,ascending = sort_parameters[mood]
       filtered_songs = songs_df[songs_df['cluster']==cluster].sort_values(by = sort_by,ascending =ascending).head(51)
    else:
       filtered_songs = songs_df.sort_values(by='track_popularity',ascending = False).head(51)

    return jsonify(filtered_songs.to_dict(orient='records'))


if __name__=="__main__":
        app.run(debug=True, port=5001)








