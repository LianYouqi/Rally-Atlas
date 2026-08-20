from pathlib import Path
import pandas as pd

DATA_DIR = Path('processed_data')
PERSONAL_DATA_PATH = DATA_DIR / 'personal.csv'

def load_sample(sample_name: str) -> pd.DataFrame:
    """Loads a processed summary CSV (written by shot_distribution_analysis.py)."""
    path = DATA_DIR / f'{sample_name}.csv'
    if not path.exists():
        raise FileNotFoundError(
            f"Couldn't find the {path}. Run procressing.py first to generate it"
        )
    df = pd.read_csv(path,index_col='shot type')
    return df

def load_personal_sample() -> pd.DataFrame:
    """Loads your own shot-distribution CSV from PERSONAL_DATA_PATH.

    Must share the schema produced by csv_generation() in
    shot_distribution_analysis.py: indexed by 'shot type', with 'count',
    'overall frequency (%)', 'forehand (count)', 'forehand ratio (%)',
    'backhand (count)', and 'backhand ratio (%)' columns. Shot types you
    haven't logged yet can simply be omitted — plot_personal_vs_elite fills
    them in as zero.
    """
    if not PERSONAL_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Couldn't find {PERSONAL_DATA_PATH}. Add your own shot-distribution"
            "CSV there (same schema as the elite sumaries) to use this view"
        )

    df = pd.read_csv(PERSONAL_DATA_PATH, index_col= 'shot type')
    return df