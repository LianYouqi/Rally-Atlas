"""
Analyzes shot-type distributions (count, frequency, forehand/backhand ratio)
for elite male and female singles badminton players from ShuttleSet match data.
"""

import argparse
from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path("raw_data")
OUTPUT_DIR = Path("processed_data_v2")

# Maps Chinese shot type labels from ShuttleSet to English equivalents
TRANSLATION = {
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
    '未知球種': 'unnamed shot',
}

WIN_LOSE = {'A': 'Winner', 'B': 'Loser'}


def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Filters, translates, and formats raw match data for analysis.

    Keeps only the 'player', 'type', and 'backhand' columns, translates shot
    type labels from Chinese to English using TRANSLATION, maps player codes
    to 'Winner'/'Loser', and converts the 'backhand' column from numeric
    (0/1) to boolean.

    Parameters:
        df: Raw match DataFrame loaded from the ShuttleSet CSV files.
            Must contain 'player', 'type', and 'backhand' columns.

    Returns:
        Cleaned DataFrame with columns:
            - 'player' (str): 'Winner' or 'Loser'
            - 'type' (str): English shot type label
            - 'backhand' (bool): True if the shot was played on the
              backhand side, False otherwise.
    """
    df = df[['player', 'type', 'backhand']].copy()
    df['player'] = df['player'].replace(WIN_LOSE)
    df['type'] = df['type'].replace(TRANSLATION)
    df['backhand'] = df['backhand'].fillna(0).astype(bool)

    return df


def shot_identification(df: pd.DataFrame) -> tuple[dict, dict, dict, dict]:
    """Counts occurrences of each shot type by forehand/backhand, split by
    whether the player went on to win or lose the match.

    Parameters:
        df: Cleaned DataFrame from data_cleaning().
            Must contain 'player' (str), 'type' (str), and 'backhand' (bool)
            columns.

    Returns:
        A 4-tuple of dicts (shot type -> count):
            (winner_forehand_counts, winner_backhand_counts,
             loser_forehand_counts, loser_backhand_counts)
    """
    counts = {
        ('Winner', False): {shot: 0 for shot in TRANSLATION.values()},
        ('Winner', True): {shot: 0 for shot in TRANSLATION.values()},
        ('Loser', False): {shot: 0 for shot in TRANSLATION.values()},
        ('Loser', True): {shot: 0 for shot in TRANSLATION.values()},
    }

    # value_counts on a groupby is much faster than iterrows() for this kind
    # of tally, since it avoids the per-row Python-level loop.
    tally = df.groupby(['player', 'backhand'])['type'].value_counts()

    for (player, is_backhand, shot_type), n in tally.items():
        if player not in ('Winner', 'Loser'):
            continue
        counts[(player, is_backhand)][shot_type] = int(n)

    return (
        counts[('Winner', False)],
        counts[('Winner', True)],
        counts[('Loser', False)],
        counts[('Loser', True)],
    )


def csv_generation(output_stem: str, forehand_counts: dict, backhand_counts: dict, win_lose: str) -> None:
    """Builds a summary DataFrame from shot-count dictionaries and writes it
    to CSV for further research use.

    Parameters:
        output_stem: Base name for the output file (e.g. 'male', 'female').
        forehand_counts: Dict mapping shot type (str) -> forehand count (int),
            from shot_identification().
        backhand_counts: Dict mapping shot type (str) -> backhand count (int),
            from shot_identification().
        win_lose: 'win' or 'lose' — which group this summary covers.

    Returns:
        None. Results are written to OUTPUT_DIR / f'{output_stem}_{win_lose}.csv'.
    """
    total = sum(forehand_counts[shot] + backhand_counts[shot] for shot in forehand_counts)

    rows = []
    for shot in forehand_counts:
        forehand = forehand_counts[shot]
        backhand = backhand_counts[shot]
        shot_total = forehand + backhand

        rows.append({
            'shot type': shot,
            'count': shot_total,
            'overall frequency (%)': 100 * shot_total / total if total else 0,

            'forehand (count)': forehand,
            'forehand ratio (%)': 100 * forehand / shot_total if shot_total else 0,

            'backhand (count)': backhand,
            'backhand ratio (%)': 100 * backhand / shot_total if shot_total else 0,
        })

    summary = pd.DataFrame(rows).set_index('shot type')
    print(summary.to_string())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f'{output_stem}_{win_lose}.csv'
    try:
        summary.to_csv(out_path)
        print(f"CSV file saved to {out_path}")
    except OSError as e:
        print(f"Error saving CSV: {e}")


def process_group(files: list[str], output_stem: str) -> None:
    """Aggregates shot counts across all match CSVs for one gender group and
    writes winner/loser summary CSVs."""
    winner_forehand = {shot: 0 for shot in TRANSLATION.values()}
    winner_backhand = {shot: 0 for shot in TRANSLATION.values()}
    loser_forehand = {shot: 0 for shot in TRANSLATION.values()}
    loser_backhand = {shot: 0 for shot in TRANSLATION.values()}

    for file in files:
        df = data_cleaning(pd.read_csv(file))
        wf, wb, lf, lb = shot_identification(df)

        for shot in wf:
            winner_forehand[shot] += wf[shot]
            winner_backhand[shot] += wb[shot]
            loser_forehand[shot] += lf[shot]
            loser_backhand[shot] += lb[shot]

    csv_generation(output_stem, winner_forehand, winner_backhand, 'win')
    csv_generation(output_stem, loser_forehand, loser_backhand, 'lose')


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize badminton shot-type distributions by gender.")
    parser.add_argument(
        'gender',
        nargs='?',
        choices=['male', 'female'],
        help="Which player group to process. If omitted, you'll be prompted.",
    )
    args = parser.parse_args()

    gender = args.gender
    while gender not in ('male', 'female'):
        gender = input("Process 'male' or 'female' player data? ").strip().lower()

    files = sorted((RAW_DATA_DIR / gender).glob("**/*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found under {RAW_DATA_DIR / gender}")

    process_group([str(f) for f in files], gender)


if __name__ == "__main__":
    main()