import pandas as pd
import os
import glob

# Actual list of badminton data
male_files = glob.glob("./raw_data/male/**/*.csv", recursive=True)
female_files = glob.glob("./raw_data/female/**/*.csv", recursive=True)

translation = {
    '放小球': 'net shot',
    '擋小球': 'return net',
    '殺球': 'smash',
    '點扣': 'wrist smash',
    '挑球': 'lift',
    '防守回挑': 'defensive return lift',
    '長球': 'clear',
    '平球': 'drive',
    '小平球': 'driven flight',
    '後場抽平球': 'back-court drive',
    '切球': 'drop',
    '過度切球': 'passive drop',
    '推球': 'push',
    '撲球': 'rush',
    '防守回抽': 'defensive return drive',
    '勾球': 'cross-court net shot',
    '發短球': 'short service',
    '發長球': 'long service',
    '未知球種': 'unnamed shot'
}
#Test Data smaller sample size
test_male_files = glob.glob('./test_data/test_male/**/*.csv', recursive=True)

def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    ''''''
    df = df[['type', 'backhand']] 
    df['type'] = df['type'].replace(translation)
    df['backhand'] = df['backhand'].fillna(0).astype(bool)

    return df

def shot_identification(df: pd.DataFrame):
    '''Counts the various shot types
    
    returns:
        forehand_shot_counts(list): The number of different shots played on the forehand side
        backhand_shot_counts(list): Shots played on the backhand side
    '''
    # Initialization of the return variables
    all_shots = translation.values()

    forehand_shot_counts = {shot: 0 for shot in all_shots}
    backhand_shot_counts = {shot: 0 for shot in all_shots}

    #Sorting
    for index, row in df.iterrows():
        shot_type = row['type']
        is_backhand = row['backhand']

        if is_backhand:
            backhand_shot_counts[shot_type] += 1
        else:
            forehand_shot_counts[shot_type] += 1

    return forehand_shot_counts, backhand_shot_counts

def csv_generation(forehand_shot_counts: dict, backhand_shot_counts: dict) -> pd.DataFrame:
    rows = []
    total = 0 

    for shot in forehand_shot_counts:
        forehand = forehand_shot_counts[shot]
        backhand = backhand_shot_counts[shot]
        total += forehand + backhand

    for shot in forehand_shot_counts:
        forehand = forehand_shot_counts[shot]
        backhand = backhand_shot_counts[shot]

        shot_total = forehand + backhand

        rows.append({
            'shot type': shot,
            'count': shot_total,
            '(%) of all shots': shot_total/total if total else 0,

            'FH (count)': forehand,
            'FH usage (%)': forehand/shot_total if shot_total else 0,

            'BH (count)': backhand,
            'BH usage (%)': backhand/shot_total if shot_total else 0,

        })
    df = pd.DataFrame(rows).set_index('shot type')

    print(df.to_string())
    # Test
    # try:
    #     df.to_csv('processed_test')
    #     print("CSV file 'processed_test' created successfully.")
    # except Exception as e:
    #     print(f"Error saving CSV: {e}")

# Main Code
overall_forehand_counts = {shot: 0 for shot in translation.values()}
overall_backhand_counts = {shot: 0 for shot in translation.values()}

for _ in female_files:
    df = pd.read_csv(_) 

    df = data_cleaning(df)
    forehand_shot_counts, backhand_shot_counts = shot_identification(df)

    for i in forehand_shot_counts:
        overall_forehand_counts[i] += forehand_shot_counts[i]
    for i in backhand_shot_counts:
        overall_backhand_counts[i] += backhand_shot_counts[i]


csv_generation(overall_forehand_counts, overall_backhand_counts)