# train_recommendation_model.py
import pandas as pd
import numpy as np
import implicit
import pickle
import os
from scipy.sparse import csr_matrix
from collections import defaultdict

def train_model_from_csv(csv_path):
    """
    Trains a collaborative filtering model using the implicit library.
    
    Args:
        csv_path: Path to the CSV file containing the survey data
    """
    print(f"Loading CSV data from {csv_path}")
    
    # Load the CSV data
    df = pd.read_csv(csv_path, encoding='latin1')
    print(f"Loaded {len(df)} records from CSV")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('"|"', '"', regex=True)
    
    # Assign unique user IDs
    df['user_id'] = ['User_' + str(i) for i in range(len(df))]
    
    # These columns contain food/drink preferences
    food_cols = [
        "What is your usual craving for Jamaican breakfast?",
        "Which of these popular Jamaican sides would you pair with your breakfast?",
        "What do you usually order for a light breakfast?",
        "Which meat type do you prefer?",
        "Which of these would you typically order for lunch?",
        "And what side dish would you choose to go with that?",
        "Which of these cooking styles or flavors do you enjoy the most in your meals?",
        "Which of these popular Jamaican Juices would you choose with your lunch?",
        "What drink would you most likely order with your lunch?",
        "Which of these smoothie combinations sounds most refreshing to you?"
    ]
    
    print("Processing interactions...")
    # Normalize and melt the data into user-item format
    interactions = []
    
    for index, row in df.iterrows():
        user = row['user_id']
        for col in food_cols:
            if col in df.columns:  # Make sure column exists
                items = str(row[col]).split(',')  # In case they selected multiple
                for item in items:
                    cleaned = item.strip()
                    if cleaned and cleaned.lower() != 'nan':
                        interactions.append((user, cleaned, 1))  # Implicit "like"
    
    interactions_df = pd.DataFrame(interactions, columns=['user_id', 'item', 'rating'])
    print(f"Created {len(interactions_df)} user-item interactions")
    
    # Create dictionaries to map users and items to/from indices
    unique_users = interactions_df['user_id'].unique()
    unique_items = interactions_df['item'].unique()
    
    print(f"Found {len(unique_users)} unique users and {len(unique_items)} unique food items")
    
    user_to_idx = {user: i for i, user in enumerate(unique_users)}
    item_to_idx = {item: i for i, item in enumerate(unique_items)}
    idx_to_user = {i: user for user, i in user_to_idx.items()}
    idx_to_item = {i: item for item, i in item_to_idx.items()}
    
    # Create sparse matrix of user-item interactions
    user_indices = [user_to_idx[user] for user in interactions_df['user_id']]
    item_indices = [item_to_idx[item] for item in interactions_df['item']]
    ratings = interactions_df['rating'].values
    
    # Create sparse matrix (users as rows, items as columns)
    sparse_user_item = csr_matrix((ratings, (user_indices, item_indices)), 
                                  shape=(len(unique_users), len(unique_items)))
    
    print("Training the model...")
    # Train the model
    model = implicit.als.AlternatingLeastSquares(factors=50, iterations=15)
    model.fit(sparse_user_item.T)  # Transpose matrix to get implicit's expected format
    
    # Save model and mapping dictionaries
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    
    with open(os.path.join(model_dir, 'implicit_model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    with open(os.path.join(model_dir, 'user_mappings.pkl'), 'wb') as f:
        pickle.dump({
            'user_to_idx': user_to_idx,
            'idx_to_user': idx_to_user,
            'item_to_idx': item_to_idx,
            'idx_to_item': idx_to_item
        }, f)
    
    with open(os.path.join(model_dir, 'all_food_items.pkl'), 'wb') as f:
        pickle.dump(list(unique_items), f)
        
    # Save feature mapping for reference
    survey_to_db_mapping = create_feature_mapping()
    with open(os.path.join(model_dir, 'feature_mapping.pkl'), 'wb') as f:
        pickle.dump(survey_to_db_mapping, f)
    
    # Also save the sparse matrix for later use
    with open(os.path.join(model_dir, 'sparse_user_item.pkl'), 'wb') as f:
        pickle.dump(sparse_user_item, f)
    
    print(f"Model trained and saved to {model_dir} directory")
    return "Model trained successfully using implicit ALS"

def create_feature_mapping():
    """
    Creates a mapping between survey questions and database columns.
    """
    # Map survey questions to database columns
    return {
        "What is your usual craving for Jamaican breakfast?": {
            "Ackee & Saltfish": "ackee_saltfish",
            "Callaloo": "callaloo",
            "Cooked up saltfish": "cooked_saltfish",
            "Kidney": "kidney",
            "Liver": "liver",
        },
        "Which of these popular Jamaican sides would you pair with your breakfast?": {
            "Fried Plantain": "fried_plantain",
            "Fry Dumpling": "dumplings",
            "Festival": "festival",
            "Breadfruit": "breadfruit",
        },
        "What do you usually order for a light breakfast?": {
            "Porridge": "porridge",
            "Scrambled Eggs": "scrambled_eggs",
            "Pancakes": "pancakes",
            "French Toast": "french_toast",
            "Waffles": "waffles",
            "Bacon": "bacon",
            "Sausage": "sausage",
            "Sandwich": "sandwich",
        },
        "Which meat type do you prefer?": {
            "Chicken": "chicken",
            "Fish": "fish",
            "Pork": "pork",
            "Goat": "goat",
            "Beef": "beef",
            "No meat": "no_meat",
        },
        "Which of these would you typically order for lunch?": {
            "Fry Chicken": "fry_chicken",
            "Bake Chicken": "bake_chicken",
            "Curry Goat": "curry_goat",
            "Soup": "soups",
            "Steamed Fish": "steamed_fish",
            "Escovitch Fish": "escovitch_fish",
            "Patty": "patty",
            "Sandwich/Burger": "sandwiches",
            "Pasta": "pasta",
        },
        "Which of these cooking styles or flavors do you enjoy the most in your meals?": {
            "Jamaican ( eg. brown stew, run down, escoveitch)": "cooking_jamaican",
            "Indian (eg. curry)": "cooking_indian",
            "Chinese (eg. stir fries)": "cooking_chinese",
            "African (eg. Pepper-pot soups)": "cooking_african",
            "Vegan/Ital": "cooking_vegan_ital",
            "Italian (eg. pasta, pizza)": "cooking_italian",
        },
        "Which of these popular Jamaican Juices would you choose with your lunch?": {
            "Pineapple Ginger Juice": "pine_ginger",
            "Callaloo Juice": "callallo_juice",
            "Juneplum Juice": "june_plum",
            "Guava pineapple Juice": "guava_pine",
            "Beetroot Juice": "beet_root",
            "Orange Juice": "orange_juice",
        }
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = "../Pelican_Eats.csv"
        
    print(f"Starting training with CSV file: {csv_path}")
    result = train_model_from_csv(csv_path)
    print(result)