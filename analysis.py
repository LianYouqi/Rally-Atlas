from load_files import load_sample, load_personal_sample
import pandas as pd
import numpy as np

from pathlib import Path
PROCESSED_DIR = Path('processed_data')
files = [f.stem for f in PROCESSED_DIR.glob('*.csv') if f.stem != 'personal']
FEATURE_COLS = ['overall frequency', 'forehand ratio', 'backhand ratio']

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
    return float(cosine_similiarity(elite_values, personal_values))

def analyze_personal_to_elite() -> dict[str, list[float]]:
    personal_df = load_personal_sample()
    personal_vecs = {col: build_feature_vector(personal_df, col) for col in FEATURE_COLS}

    results = {}
    for csv_name in files:
        df = load_sample(csv_name)
        results[csv_name] = [
            compute_cos_sim(build_feature_vector(df, col), personal_vecs[col])
            for col in FEATURE_COLS
        ]
    return results

def summary():
    results = analyze_personal_to_elite()

    df = pd.DataFrame.from_dict(results, orient='index', columns=FEATURE_COLS)
    df.index.name = 'your sample'
    df = df.sort_values(by=FEATURE_COLS[0], ascending=False)
    print("=" * 50)
    print("Unformated Results")
    print("=" * 50)
    print(df.to_string())

    print("\n" + "=" * 50)
    print("Personal Gameplay vs. Elite Player Comparison")
    print("=" * 50)

    for csv_name, scores in results.items():
        label = csv_name.replace('_', ' ').title()
        print(f"\n{label}")
        print("-" * len(label))
        for feature, score in zip(FEATURE_COLS, scores):
            print(f"  {feature:<20} similarity: {score:.4f}")

    print("\n" + "=" * 50)
    print("Closest Matches")
    print("=" * 50)
    for i, feature in enumerate(FEATURE_COLS):
        best_match = max(results, key=lambda k: results[k][i])
        best_score = results[best_match][i]
        print(f"  {feature:<20} -> {best_match.replace('_', ' ').title()} ({best_score:.4f})")


def main():
    pass

summary()