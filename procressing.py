import pandas as pd
import os
import glob

# Actual list of badminton data
# male_files = glob.glob("./raw_data/male/**/*.csv", recursive=True)
# female_files = glob.glob("./raw_data/female/**/*.csv", recursive=True)

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
    '發長球': 'long service'
}

#Accumulators
overall_shot_counts = {shot: 0 for shot in translation.values()}
overall_forehand_counts = {shot: 0 for shot in translation.values()}
overall_backhand_counts = {shot: 0 for shot in translation.values()}


#Test Data smaller sample size
test_male_files = glob.glob('./test_data/test_male/**/*.csv', recursive=True)

def shot_identification(df: pd.DataFrame):
    '''Counts the various shot types
    
    returns:
        shot_counts(list): The number of shots played without the account of forehand or backhand
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

    shot_counts = {
        key: forehand_shot_counts[key] + backhand_shot_counts[key] for key in forehand_shot_counts
    }

    return shot_counts, forehand_shot_counts, backhand_shot_counts

def csv_generation()
# Main Code


for i in test_male_files:
    df = pd.read_csv(i) 
    df = df[['type', 'backhand']] #Selecting only 'shot type' and 'backhand' columns

    #Data cleaning
    df['type'] = df['type'].replace(translation)
    df['backhand'] = df['backhand'].fillna(0).astype(bool)

    shot_counts, forehand_shot_counts, backhand_shot_counts = shot_identification(df)

    for i in shot_counts:
        overall_shot_counts[i] += shot_counts[i]
    for i in forehand_shot_counts:
        overall_forehand_counts[i] += forehand_shot_counts[i]
    for i in backhand_shot_counts:
        overall_backhand_counts[i] += backhand_shot_counts[i]


overall_shot_counts = pd.DataFrame(
    overall_shot_counts.items(),
    columns= ['shot type', 'count']
    )

overall_backhand_counts = pd.DataFrame(
    overall_backhand_counts.items(),
    columns= ['shot type (backhand)', 'count']
)

overall_forehand_counts = pd.DataFrame(
    overall_forehand_counts.items(),
    columns= ['shot type (forehand)', 'count']
)


print(overall_shot_counts)
print(overall_backhand_counts)
print(overall_forehand_counts)