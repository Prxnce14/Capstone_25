import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommend_items(user_index, user_item_matrix, mlb, top_n=5):
    # Compute similarity between users
    similarity_matrix = cosine_similarity(user_item_matrix)

    # Get the most similar users
    user_similarities = similarity_matrix[user_index]
    similar_users_idx = np.argsort(user_similarities)[::-1][1:]  # exclude self

    # Sum preferences of similar users
    scores = np.sum(user_item_matrix[similar_users_idx], axis=0)

    # Remove items the user already likes
    user_likes = user_item_matrix[user_index]
    scores = scores * (1 - user_likes)

    # Recommend top N items
    top_indices = np.argsort(scores)[::-1][:top_n]
    recommended_items = [mlb.classes_[i] for i in top_indices]

    return recommended_items