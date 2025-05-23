# recommendation_helper.py
import os
import pickle
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from collections import defaultdict
from scipy.sparse import csr_matrix

def get_user_food_recommendations(user_id, n=5):
    """
    Generate food recommendations based on user preferences stored in the database.
    
    Args:
        user_id: Database ID of the user
        n: Number of recommendations to return per category
        
    Returns:
        Dict with food recommendations
    """
    # Load the model and supporting data
    try:
        model_dir = 'models'
        model_path = os.path.join(model_dir, 'implicit_model.pkl')
        mappings_path = os.path.join(model_dir, 'user_mappings.pkl')
        foods_path = os.path.join(model_dir, 'all_food_items.pkl')
        feature_mapping_path = os.path.join(model_dir, 'feature_mapping.pkl')
        
        if not all(os.path.exists(p) for p in [model_path, mappings_path, foods_path, feature_mapping_path]):
            return {"error": "Recommendation model files not available. Did you run the training script?"}
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(mappings_path, 'rb') as f:
            mappings = pickle.load(f)
            item_to_idx = mappings['item_to_idx']
            idx_to_item = mappings['idx_to_item']
        
        with open(foods_path, 'rb') as f:
            all_foods = pickle.load(f)
        
        with open(feature_mapping_path, 'rb') as f:
            feature_mapping = pickle.load(f)
    except Exception as e:
        return {"error": f"Error loading model files: {str(e)}"}
    
    # Connect to database using your connection pattern
    try:
        stores = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/pelicandb')
        engine = create_engine(stores)
        
        # Query for this user's preferences
        with engine.connect() as connection:
            query = f"SELECT * FROM user_preferences WHERE user_id = {user_id} LIMIT 1"
            user_prefs = pd.read_sql(query, connection)
            
            if len(user_prefs) == 0:
                return {"message": "No preferences found for this user"}
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}
    
    # Convert DB preferences to survey item format
    user_items = []
    
    # Reverse the mapping to go from DB columns to survey items
    db_to_survey_items = {}
    for category, mappings in feature_mapping.items():
        for survey_item, db_column in mappings.items():
            db_to_survey_items[db_column] = survey_item
    
    # Get boolean columns that are True for this user
    user_row = user_prefs.iloc[0]
    active_preferences = []
    
    for col in user_row.index:
        if col in db_to_survey_items and user_row[col] == True:
            active_preferences.append(col)
    
    # Convert to survey items
    for db_col in active_preferences:
        if db_col in db_to_survey_items:
            user_items.append(db_to_survey_items[db_col])
    
    # Also add free-form text preferences that might be comma-separated
    for text_field in ['liked_foods', 'other_meat', 'other_breakfast_items', 'other_lunch', 'other_juice']:
        if text_field in user_row and not pd.isna(user_row[text_field]) and user_row[text_field]:
            for item in str(user_row[text_field]).split(','):
                user_items.append(item.strip())
    
    # If the user has no recognized items, return an empty result
    if not user_items:
        return {"message": "No recognized food preferences found for recommendations"}
    
    # Create vector of user's preferences mapped to the model's items
    user_vector = np.zeros(len(all_foods))
    recognized_items = []
    
    for item in user_items:
        if item in item_to_idx:
            user_vector[item_to_idx[item]] = 1
            recognized_items.append(item)
    
    # If no recognized items match the training data, return an appropriate message
    if not recognized_items:
        return {"message": "User preferences don't match any items in the training data"}
    
    # Convert to sparse matrix format 
    user_vector_sparse = csr_matrix(user_vector)
    
    # Get similar items based on this user's preferences
    similar_items = []
    for item in recognized_items:
        if item in item_to_idx:
            item_idx = item_to_idx[item]
            # Get related items from the model
            related = model.similar_items(item_idx, N=n+1)  # +1 because the item itself will be included
            # Skip the first one (the item itself)
            for idx, score in related[1:]:
                similar_items.append((idx_to_item[idx], score, item))
    
    # Sort by score and get unique recommendations
    similar_items.sort(key=lambda x: x[1], reverse=True)
    
    # Group recommendations by category
    categorized_recs = defaultdict(list)
    
    for category in feature_mapping.keys():
        category_items = []
        for rec_item, score, based_on in similar_items:
            # Check if the item and what it's based on belong to this category
            item_in_category = False
            for survey_item in feature_mapping[category].keys():
                if rec_item in survey_item or survey_item in rec_item:
                    item_in_category = True
                    break
            
            if item_in_category and rec_item not in recognized_items:
                if rec_item not in [i[0] for i in category_items]:
                    category_items.append((rec_item, score, based_on))
        
        # Get top N for this category
        category_items = category_items[:n]
        if category_items:
            categorized_recs[category] = category_items
    
    # Format the results for a better user experience
    formatted_recommendations = {}
    
    for category, items in categorized_recs.items():
        if items:
            category_items = []
            based_on_items = set()
            
            for item, _, based_on in items:
                category_items.append(item)
                based_on_items.add(based_on)
            
            based_on_str = ", ".join(based_on_items)
            recommended_str = ", ".join(category_items)
            
            formatted_recommendations[category] = {
                "user_selected": based_on_str,
                "recommended": recommended_str,
                "message": f"Based on your preference for {based_on_str}, you might also enjoy {recommended_str}"
            }
    
    # If we found no recommendations
    if not formatted_recommendations:
        return {"message": "Could not generate specific recommendations for your preferences"}
    
    return formatted_recommendations