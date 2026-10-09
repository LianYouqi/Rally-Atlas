from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / 'processed_data'
PERSONAL_DATA_PATH = DATA_DIR / 'personal.csv'

def load_sample(sample_name: str) -> pd.DataFrame:
    """Loads a processed summary CSV written by procressing.py."""
    path = DATA_DIR / f'{sample_name}.csv'
    if not path.exists():
        raise FileNotFoundError(
            f"Couldn't find the {path}. Run procressing.py first to generate it"
        )
    df = pd.read_csv(path,index_col='shot type')
    return df

def load_personal_sample() -> pd.DataFrame:
    """Loads your own shot-distribution CSV from PERSONAL_DATA_PATH.

    Must share the schema produced by procressing.py: indexed by 'shot type',
    with 'count', 'forehand', 'backhand', 'overall frequency',
    'forehand ratio', and 'backhand ratio' columns.
    """
    if not PERSONAL_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Couldn't find {PERSONAL_DATA_PATH}. Add your own shot-distribution"
            "CSV there (same schema as the elite sumaries) to use this view"
        )

    df = pd.read_csv(PERSONAL_DATA_PATH, index_col= 'shot type')
    return df