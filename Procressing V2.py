import pandas as pd
import glob as glob

import pandas as pd
import glob

male_files = glob.glob("./raw_data/male/**/*.csv", recursive=True)
test_sample = male_files[0]
female_files = glob.glob("./raw_data/female/**/*.csv", recursive=True)

# Maps Chinese shot type labels from ShuttleSet to English equivalents
#[[[]]]
translation = {
    '放小球': 'net shot',
    '擋小球': 'return net',
    '殺球': 'smash',
    '點扣': 'wrist smash',
    '挑球': 'lift',
    '防守回挑': 'defensive return lob',
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

def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Filters, translates, and formats raw match data for analysis

    Keeps only the 'type' and 'back' columns, translates shot type labels
    from Chinese to English using the TRANSLATION dictionary and converts
    the 'backhand' column from numeric (0/1) to boolean

    Parameters:
        df: Raw match DataFrame laoded from the ShuttleSet CSV files.
            Must contain 'type' and 'backhand' columns
    
    Returns:
        df: Cleaned DataFrame with two columns:
            - 'type' (str): English shot type label
            - 'backhand' (bool): True if the shot was played on the 
               backhand side, False otherwise.  
    """
    win_lose = {
        'A': 'Winner',
        'B': 'Loser'
    }
    df = df[['player', 'type', 'backhand']] 
    df['player'] = df['player'].replace(win_lose)
    df['type'] = df['type'].replace(translation)
    df['backhand'] = df['backhand'].fillna(0).astype(bool)

    return df

def shot_identification(df: pd.DataFrame) -> dict:
    """Counts the occurances of each type of badminton shot by forehand and backhand and categorizing 
    them by player's result after the match (win/lose)

    Parameters:
        df: Cleaned DataFrame from data_cleaning function.
            Must contain 'player' (str), 'type' (str), and 'backhand' (bool) columns
    
    Returns:
        player_A_forehand_shot_counts: Dictionary mapping each shot type (str) to its forehand count (int)
        player_A_backhand_shot_counts: Dictionary mapping each shot type (str) to its backhand count (int)
        player_B_forehand_shot_counts: Dictionary mapping each shot type (str) to its forehand count (int)
        player_B_backhand_shot_counts: Dictionary mapping each shot type (str) to its backhand count (int)
    """
    # Initialization of the return variables
    all_shots = translation.values()

    player_A_forehand_shot_counts = {shot: 0 for shot in all_shots}
    player_A_backhand_shot_counts = {shot: 0 for shot in all_shots}
    player_B_forehand_shot_counts = {shot: 0 for shot in all_shots}
    player_B_backhand_shot_counts = {shot: 0 for shot in all_shots}

    #Sorting
    for index, row in df.iterrows():
        shot_type = row['type']
        is_backhand = row['backhand']
        player = row['player']

        match player:
            case 'Winner':
                if is_backhand:
                    player_A_backhand_shot_counts[shot_type] += 1
                else:
                    player_A_forehand_shot_counts[shot_type] += 1

            case 'Loser':
                if is_backhand:
                    player_B_backhand_shot_counts[shot_type] += 1
                else:
                    player_B_forehand_shot_counts[shot_type] += 1

            case _:
                continue

    return (
        player_A_forehand_shot_counts,
        player_A_backhand_shot_counts,
        player_B_forehand_shot_counts,
        player_B_backhand_shot_counts
    )

def csv_generation(output_path_name: str, forehand_counts: dict, backhand_counts: dict, win_lose: str) -> None:
    """Ultizes the dictionary maping of each shot type from shot_identification function and generates
       a clean, processed Panda's DataFrame containing statistics for further research purposes.

    Parameters:
        output_path_name: The name of the CSV file
        forehand_counts: Dictionary mapping of shot type (str) and its forehand count (int).
                              Generated from shot_idenitifcation function.
        backhand_counts: Dictionary mapping of shot type (str) and its backhand count (int).
                              Generated from shot_idenitifcation function.
        win_lose: Which CSV file does it belong to: Winner/Loser

    Returns:
        None: Results are saved to a CSV file at the specified output_path_name
    """
    rows = []
    total = 0 

    # Calculates grand total for pecentage computation
    for shot in forehand_counts:
        forehand = forehand_counts[shot]
        backhand = backhand_counts[shot]
        total += forehand + backhand

    # Constructing rows using percentages conditioned to the grand total
    for shot in forehand_counts:
        forehand = forehand_counts[shot]
        backhand = backhand_counts[shot]

        shot_total = forehand + backhand

        rows.append({
            'shot type': shot,
            'count': shot_total,
            'overall frequency': shot_total/total if total else 0,

            'forehand (count)': forehand,
            'forehand ratio (%)': forehand/shot_total if shot_total else 0,

            'backhand (count)': backhand,
            'backhand ratio (%)': backhand/shot_total if shot_total else 0,
        })
    df = pd.DataFrame(rows).set_index('shot type')

    print(df.to_string())

    try:
        df.to_csv(f'processed_data V2/{output_path_name}_{win_lose}')
        print("CSV file created successfully.")
    except Exception as e:
        print(f"Error saving CSV: {e}")

# Main Code
# Prompt user to select gender group
gender = input(
    "Which dataset group of professional singles badminton player would you like to process?\n" \
    "For 'Professional Male Badminton Althetes', type 'male'\n" \
    "For 'Professional Female Badminton Althetes', type 'female'\n" \
    ":  "
    )
output_path_name = None

if gender.lower() == 'male':
    gender = male_files
    output_path_name = 'male'
elif gender.lower() == 'female':
    gender = female_files
    output_path_name = 'female'
else:
    raise ValueError(f'gender must be either male or female, got {gender}')

overall_winner_forehand_counts = {shot: 0 for shot in translation.values()}
overall_winner_backhand_counts = {shot: 0 for shot in translation.values()}
overall_loser_forehand_counts = {shot: 0 for shot in translation.values()}
overall_loser_backhand_counts = {shot: 0 for shot in translation.values()}

# Aggregate shot counts across all match (CSV) files
for file in gender: 
    df = pd.read_csv(file) 

    df = data_cleaning(df)
    winner_forehand_counts, winner_backhand_counts, loser_forehand_counts, loser_backhand_counts = shot_identification(df)

    for i in winner_forehand_counts:
        overall_winner_forehand_counts[i] += winner_forehand_counts[i]
    for i in winner_backhand_counts:
        overall_winner_backhand_counts[i] += winner_backhand_counts[i]
    for i in loser_forehand_counts:
        overall_loser_forehand_counts[i] += loser_forehand_counts[i]
    for i in loser_backhand_counts:
        overall_loser_backhand_counts[i] += loser_backhand_counts[i]

csv_generation(
    output_path_name,
    overall_winner_forehand_counts,
    overall_winner_backhand_counts,
    'win'
    )
csv_generation(
    output_path_name,
    overall_loser_forehand_counts,
    overall_loser_backhand_counts,
    'lose'
)