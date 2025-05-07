import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

def load_and_process_data(csv_path):
    # Load the survey data with encoding handling
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')  # Use ISO-8859-1 encoding

    # Print column names for debugging
    print("Columns in CSV:", df.columns)

    # Strip any leading or trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Select columns relevant to preferences (customize if needed)
    preference_cols = [
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
    

    # Fill missing data
    df[preference_cols] = df[preference_cols].fillna('')

    # Convert multiple responses in one cell to lists (e.g., split by commas)
    for col in preference_cols:
        df[col] = df[col].apply(lambda x: [i.strip() for i in x.split(',')] if isinstance(x, str) else [])

    # Combine into a single user-item dataset
    df['all_preferences'] = df[preference_cols].sum(axis=1)

    # Use MultiLabelBinarizer to create a user-item matrix
    mlb = MultiLabelBinarizer()
    user_item_matrix = mlb.fit_transform(df['all_preferences'])
    matrix_df = pd.DataFrame(user_item_matrix, columns=mlb.classes_)

    return matrix_df, mlb