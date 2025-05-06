from preprocess import load_and_process_data
from CF_recommender import recommend_items

# Load data
matrix, mlb = load_and_process_data('app/data/pelican_eats_survey_data.csv')

# Choose a user index to test (e.g., 0 is the first person in the survey)
user_index = 25

# Get recommendations
recommended = recommend_items(user_index, matrix.values, mlb, top_n=5)

print("Recommended items for user", user_index)
print(recommended)