from load_files import load_sample, load_personal_sample
import pandas as pd
import numpy as np

from pathlib import Path
PROCESSED_DIR = Path('processed_data')
files = [f.stem for f in PROCESSED_DIR.glob('*.csv') if f.stem != 'personal']
COL_OVERALL_FREQ, COL_FH_RATIO, COL_BH_RATIO = ['overall frequency', 'forehand ratio', 'backhand ratio']

def build_feature_vector(df: pd.DataFrame, feature_col: str) -> pd.DataFrame:
    """one frequency value per shot type, indexed by shot type name"""
    return df[feature_col]

def align_vectors(elite_vec: pd.DataFrame, personal_vec: pd.DataFrame) -> pd.Series:
    combined = pd.concat([elite_vec, personal_vec], axis=1, keys=['a', 'b']).fillna(0)
    return combined['a'].values, combined['b'].values

def cosine_similiarity(a,b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    dot = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def compute_cos_sim(elite_vec: pd.DataFrame, personal_vec: pd.DataFrame) -> np.float64:
    elite_values, personal_values = align_vectors(elite_vec, personal_vec)
    return cosine_similiarity(elite_values, personal_values)


personal_df = load_personal_sample()
personal_overall_freq = build_feature_vector(personal_df, COL_OVERALL_FREQ)
personal_fh_ratio = build_feature_vector(personal_df, COL_FH_RATIO)
personal_bh_ratio = build_feature_vector(personal_df, COL_BH_RATIO)

results = {}

for csv_name in files:
    df = load_sample(csv_name)

    overall_freq =  build_feature_vector(df, COL_OVERALL_FREQ)
    fh_ratio = build_feature_vector(df, COL_FH_RATIO)
    bh_ratio = build_feature_vector(df, COL_BH_RATIO)

    overall_freq_sim = compute_cos_sim(overall_freq, personal_overall_freq)
    fh_ratio_sim = compute_cos_sim(fh_ratio, personal_fh_ratio)
    bh_ratio_sim = compute_cos_sim(bh_ratio,personal_bh_ratio)

    results[csv_name] = [overall_freq_sim,fh_ratio_sim,bh_ratio_sim]