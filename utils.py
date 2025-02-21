import pandas as pd

def get_recommendations(song_name, songs_df, similarity):

    # Get the index of the song from the DataFrame
    index = songs_df[songs_df['track_name'] == song_name].index[0]

    # Get similarity scores for the given song and enumerate them with indices
    similarity_scores = list(enumerate(similarity[index]))

    # Sort similarity scores in descending order and take the top 10 most similar songs (excluding itself)
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:11]

    recommendations = []
    
    # Iterate over the top similar songs and retrieve their details
    for i, song_details in enumerate(similarity_scores):
        song_info = songs_df.iloc[song_details[0]].to_dict()  # Convert song row to dictionary
        song_info['similarity_score'] = round(song_details[1], 3)  # Round similarity score for better readability
        recommendations.append(song_info)  # Append song info to the recommendations list

    return recommendations  # Return the list of recommended songs
