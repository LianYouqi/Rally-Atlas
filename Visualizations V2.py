"""
Plots shot-type distributions (count, frequency, forehand/backhand ratio)
for elite male and female singles badminton players, using the summary
CSVs produced by shot_distribution_analysis.py.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path("processed_data_v2")
PERSONAL_DATA_PATH = DATA_DIR / "personal.csv"

# ── Palette ──────────────────────────────────────────────────────────────────
COURT_TEAL = '#1B998B'
SMASH_RED = '#E84855'
BACKGROUND = '#0F1923'
SURFACE = '#1C2B36'
TEXT = '#E8EDF2'
GRID = '#2A3F4E'

# ── Style ────────────────────────────────────────────────────────────────────
BAR_CUSTOMIZATIONS = {
    'color': COURT_TEAL,
    'edgecolor': BACKGROUND,
    'linewidth': 0.6,
    'height': 0.65,
}

STAT_LABELS = {
    ('count', 'overall frequency (%)'): 'shot types',
    ('forehand (count)', 'forehand ratio (%)'): 'forehand plays',
    ('backhand (count)', 'backhand ratio (%)'): 'backhand plays',
}

# (menu label, csv stem) — reused for both the first- and second-sample prompts
SAMPLE_OPTIONS = {
    '1': ('male (win)', 'male_win'),
    '2': ('male (lose)', 'male_lose'),
    '3': ('female (win)', 'female_win'),
    '4': ('female (lose)', 'female_lose'),
}

STATISTIC_OPTIONS = {
    '1': ('count', 'overall frequency (%)'),
    '2': ('forehand (count)', 'forehand ratio (%)'),
    '3': ('backhand (count)', 'backhand ratio (%)'),
}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strips stray whitespace — including non-breaking spaces, which Excel
    and copy-paste sometimes smuggle in — from column names. Prevents
    confusing KeyErrors on columns that look correct when you eyeball them."""
    df.columns = [str(c).replace('\xa0', ' ').strip() for c in df.columns]
    return df


REQUIRED_SAMPLE_COLUMNS = [
    'count', 'overall frequency (%)',
    'forehand (count)', 'forehand ratio (%)',
    'backhand (count)', 'backhand ratio (%)',
]


def _coerce_legacy_frequency_column(df: pd.DataFrame) -> pd.DataFrame:
    """Accepts CSVs built against an earlier version of this project that
    used 'overall frequency' as a 0-1 fraction, instead of the current
    'overall frequency (%)' 0-100 percentage column. Converts in place so
    older personal.csv files don't need to be hand-edited."""
    if 'overall frequency (%)' not in df.columns and 'overall frequency' in df.columns:
        df = df.copy()
        df['overall frequency (%)'] = df['overall frequency'] * 100
    return df


def load_sample(stem: str) -> pd.DataFrame:
    """Loads a processed summary CSV (written by shot_distribution_analysis.py)."""
    path = DATA_DIR / f'{stem}.csv'
    if not path.exists():
        raise FileNotFoundError(
            f"Couldn't find {path}. Run shot_distribution_analysis.py first to generate it."
        )
    df = _normalize_columns(pd.read_csv(path, index_col='shot type'))
    return _coerce_legacy_frequency_column(df)


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
            f"Couldn't find {PERSONAL_DATA_PATH}. Add your own shot-distribution "
            "CSV there (same schema as the elite summaries) to use this view."
        )
    df = _normalize_columns(pd.read_csv(PERSONAL_DATA_PATH, index_col='shot type'))
    df = _coerce_legacy_frequency_column(df)

    missing = [c for c in REQUIRED_SAMPLE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"personal.csv is missing columns {missing}. "
            f"Columns found: {list(df.columns)}."
        )
    return df


def _draw_bar_chart(ax: plt.Axes, df_sorted: pd.DataFrame, metric: str, title: str) -> None:
    """Draws one horizontal bar chart of `metric` on `ax`, annotated with
    count and overall-frequency percentage, highlighting the top bar."""
    ax.set_facecolor(SURFACE)
    bars = ax.barh(df_sorted.index, df_sorted[metric], **BAR_CUSTOMIZATIONS)

    if not bars:
        return

    max_val = df_sorted[metric].max()
    if max_val > 0:
        # Highlight whichever bar is actually largest, rather than assuming
        # the data is sorted ascending (plot_personal_vs_elite deliberately
        # isn't, so it can line panels up by shot type instead).
        bars[df_sorted[metric].values.argmax()].set_color(SMASH_RED)

    for bar, (_, row) in zip(bars, df_sorted.iterrows()):
        width = bar.get_width()
        ax.text(
            width + max_val * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f'{int(row["count"]):,}  ({row["overall frequency (%)"]:.1f}%)',
            va='center', ha='left',
            fontsize=8, color=TEXT,
        )

    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(axis='x', color=GRID, linestyle='--', linewidth=0.5)
    ax.set_title(title, fontsize=12)
    ax.set_ylabel('Shot type', fontsize=11)


def plot_elite_distribution(sample: tuple[str, pd.DataFrame], statistic: tuple[str, str]) -> tuple[plt.Figure, plt.Axes]:
    """
    View 1: single-gender elite distribution of a particular statistic.

    Parameters:
        sample: (label, DataFrame) pair, e.g. ('male (win)', male_win_df).
                DataFrame must contain the chosen metric column and
                'overall frequency (%)' (for annotation).
        statistic: Tuple of two column names; only the first is used as the
                   metric to plot. Valid pairs are the keys of STATISTIC_OPTIONS.

    Returns:
        fig, ax: Matplotlib figure and axes objects.
    """
    metric = statistic[0]
    sample_name, df = sample
    df_sorted = df.sort_values(by=metric, ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(BACKGROUND)

    title = f'Distribution of {STAT_LABELS[statistic]} among elite {sample_name} singles players'
    _draw_bar_chart(ax, df_sorted, metric, title)
    ax.set_xlabel(metric, fontsize=12)

    plt.tight_layout()
    plt.show()
    return fig, ax


def plot_comparison(sample_one: tuple[str, pd.DataFrame], sample_two: tuple[str, pd.DataFrame], statistic: tuple[str, str]) -> tuple[plt.Figure, plt.Axes]:
    """
    View 2: distributions of two samples stacked for comparison of a
    particular statistic (e.g. elite male vs. elite female).

    Parameters:
        sample_one: (label, DataFrame) pair for the first sample.
        sample_two: (label, DataFrame) pair for the second sample.
        statistic: Tuple of two column names; only the first is used as the
                   metric to plot. Valid pairs are the keys of STATISTIC_OPTIONS.

    Returns:
        fig, axes: Matplotlib figure and axes objects.
    """
    metric = statistic[0]
    sample_one_name, df_one = sample_one
    sample_two_name, df_two = sample_two
    df_one_sorted = df_one.sort_values(by=metric, ascending=True)
    df_two_sorted = df_two.sort_values(by=metric, ascending=True)

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    fig.patch.set_facecolor(BACKGROUND)

    _draw_bar_chart(axes[0], df_one_sorted, metric, sample_one_name)
    _draw_bar_chart(axes[1], df_two_sorted, metric, sample_two_name)
    axes[1].set_xlabel(metric, fontsize=12)

    fig.suptitle(
        f'Distribution of {STAT_LABELS[statistic]}: {sample_one_name} vs {sample_two_name} singles players',
        fontsize=14, color=TEXT,
    )

    plt.tight_layout()
    plt.show()
    return fig, axes


def plot_personal_vs_elite(personal: tuple[str, pd.DataFrame], elite: tuple[str, pd.DataFrame], statistic: tuple[str, str]) -> tuple[plt.Figure, plt.Axes]:
    """
    View 3: your own shot distribution vs. an elite group, for a particular
    statistic.

    Unlike plot_comparison, both panels use the *elite* group's sort order
    (rather than each being sorted independently), so the same shot type
    lands at the same height in both charts and is easy to compare directly.

    Parameters:
        personal: (label, DataFrame) pair for your own shot data. Must share
                  the schema described in load_personal_sample(). Shot types
                  missing from your data are treated as zero.
        elite: (label, DataFrame) pair for the elite comparison group.
        statistic: Tuple of two column names; only the first is used as the
                   metric to plot. Valid pairs are the keys of STATISTIC_OPTIONS.

    Returns:
        fig, axes: Matplotlib figure and axes objects.
    """
    metric = statistic[0]
    personal_name, personal_df = personal
    elite_name, elite_df = elite

    elite_sorted = elite_df.sort_values(by=metric, ascending=True)
    # Align your data to the elite chart's shot-type order, filling any shot
    # types you haven't logged yet with zero rather than dropping them.
    personal_aligned = personal_df.reindex(elite_sorted.index).fillna(0)

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    fig.patch.set_facecolor(BACKGROUND)

    _draw_bar_chart(axes[0], personal_aligned, metric, personal_name)
    _draw_bar_chart(axes[1], elite_sorted, metric, elite_name)
    axes[1].set_xlabel(metric, fontsize=12)

    fig.suptitle(
        f'Distribution of {STAT_LABELS[statistic]}: {personal_name} vs {elite_name}',
        fontsize=14, color=TEXT,
    )

    plt.tight_layout()
    plt.show()
    return fig, axes


def prompt_choice(prompt: str, options: dict[str, tuple]) -> tuple:
    """Prints `prompt`, reads a menu key, and returns the matching value from
    `options`. Re-prompts on invalid input instead of raising immediately,
    so a typo doesn't kill an interactive session."""
    choice = input(f'{prompt}Enter choice: ').strip()
    while choice not in options:
        choice = input(f"'{choice}' isn't a valid option. Try again: ").strip()
    return options[choice]


def prompt_sample(label: str = "sample") -> tuple[str, pd.DataFrame]:
    """Prompts for one of SAMPLE_OPTIONS and loads the corresponding CSV."""
    prompt = (
        f"\nWhich group of professional singles players would you like as your {label}?\n"
        "1: Male winners\n"
        "2: Male losers\n"
        "3: Female winners\n"
        "4: Female losers\n"
    )
    name, stem = prompt_choice(prompt, SAMPLE_OPTIONS)
    return name, load_sample(stem)


def main() -> None:
    prompt_statistic = (
        "\nWhich statistic would you like to analyze?\n"
        "1: Overall shot count and frequency\n"
        "2: Forehand count and ratio\n"
        "3: Backhand count and ratio\n"
    )
    prompt_distribution = (
        "\nWhich distribution would you like to plot?\n"
        "1: Shot distribution for one elite group\n"
        "2: Shot distributions compared by gender and winning status\n"
        "3: Personal shot distribution vs. an elite group\n"
    )

    statistic = prompt_choice(prompt_statistic, STATISTIC_OPTIONS)
    sample_one = prompt_sample("first sample")

    distribution = input(f'{prompt_distribution}Enter choice: ').strip()
    match distribution:
        case '1':
            plot_elite_distribution(sample_one, statistic)
        case '2':
            sample_two = prompt_sample("second sample")
            plot_comparison(sample_one, sample_two, statistic)
        case '3':
            personal = ("me", load_personal_sample())
            plot_personal_vs_elite(personal, sample_one, statistic)
        case _:
            raise ValueError('Invalid option')


if __name__ == "__main__":
    main()