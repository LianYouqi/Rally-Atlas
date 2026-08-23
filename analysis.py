from load_files import load_sample, load_personal_sample
import pandas as pd
import numpy as np

from pathlib import Path
PROCESSED_DIR = Path('processed_data')
files = [f.stem for f in PROCESSED_DIR.glob('*.csv') if f.stem != 'personal']
FEATURE_COLS = ['overall frequency', 'forehand ratio', 'backhand ratio']

def build_feature_vector(df: pd.DataFrame, feature_col: str) -> pd.Series:
    """Extract a single feature column as a per-shot-type vector.

    Args:
        df: DataFrame indexed or containing rows by shot type, with one
            or more feature columns (e.g. overall frequency, ratios).
        feature_col: Name of the column to extract.

    Returns:
        The requested column as a Series, indexed by shot type.
    """
    return df[feature_col]

def align_vectors(elite_vec: pd.DataFrame, personal_vec: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Align two shot-type-indexed vectors on a shared index.

    Missing shot types in either vector are filled with 0 so both
    outputs have matching length and order.

    Args:
        elite_vec: Feature vector for an elite sample, indexed by shot type.
        personal_vec: Feature vector for the personal sample, indexed by shot type.

    Returns:
        A tuple of two numpy arrays (elite_values, personal_values),
        aligned on the same shot-type index.
    """
    combined = pd.concat([elite_vec, personal_vec], axis=1, keys=['a', 'b']).fillna(0)
    return combined['a'].values, combined['b'].values

def cosine_similiarity(a, b):
    """Compute the cosine similarity between two numeric vectors.

    Args:
        a: First vector (array-like).
        b: Second vector (array-like), same length as a.

    Returns:
        Cosine similarity as a float in [-1, 1]. Returns 0.0 if either
        vector has zero norm (to avoid division by zero).
    """
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def compute_cos_sim(elite_vec: pd.DataFrame, personal_vec: pd.DataFrame) -> np.float64:
    """Align two feature vectors and compute their cosine similarity.

    Args:
        elite_vec: Feature vector for an elite sample, indexed by shot type.
        personal_vec: Feature vector for the personal sample, indexed by shot type.

    Returns:
        Cosine similarity between the aligned vectors, as a plain float.
    """
    elite_values, personal_values = align_vectors(elite_vec, personal_vec)
    return float(cosine_similiarity(elite_values, personal_values))

def analyze_personal_to_elite() -> dict[str, list[float]]:
    """Compare the personal sample to every elite sample on each feature.

    Loads the personal sample once, then for each elite CSV in
    `processed_data/` computes cosine similarity against the personal
    sample for every column in FEATURE_COLS.

    Returns:
        A dict mapping each elite sample name (CSV stem) to a list of
        similarity scores, in the same order as FEATURE_COLS.
    """
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
    """Print a formatted comparison report of personal vs. elite samples.

    Runs `analyze_personal_to_elite()` and prints the results three ways:
    a raw table sorted by the first feature column, a per-sample
    breakdown of similarity scores, and a "closest match" summary
    showing which elite sample scores highest on each feature.

    Returns:
        None. Output is printed directly to stdout.
    """
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