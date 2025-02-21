import pandas as pd

def get_recommendations(song_name,songs_df,similarity):

    index=songs_df[songs_df['track_name'] == song_name].index[0]
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores,key= lambda x:x[1],reverse=True)[1:11]

    recommendations = []
    for i,song_details in enumerate(similarity_scores):
        song_info = songs_df.iloc[song_details[0]].to_dict()
        song_info['similarity_score'] = round(song_details[1], 3)
        recommendations.append(song_info)

    return recommendations
