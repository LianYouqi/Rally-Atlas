import matplotlib.pyplot as plt
import pandas as pd

male_win_df   = pd.read_csv('processed_data V2/male_win',   index_col='shot type')
male_lose_df = pd.read_csv('processed_data V2/male_lose', index_col='shot type')
female_win_df = pd.read_csv('processed_data V2/female_win', index_col='shot type')
female_lose_df = pd.read_csv('processed_data V2/female_lose', index_col='shot type')
personal_df = None

# ── Palette ───────────────────────────────────────────────────────────────────
COURT_TEAL  = '#1B998B'
SMASH_RED   = '#E84855'
BACKGROUND  = '#0F1923'
SURFACE     = '#1C2B36'
TEXT        = '#E8EDF2'
GRID        = '#2A3F4E'

# ── Style ─────────────────────────────────────────────────────────────────────
BAR_CUSTOMIZATIONS = {
    'color':     COURT_TEAL,
    'edgecolor': BACKGROUND,
    'linewidth': 0.6,
    'height':    0.65,
}

STAT_LABELS = {
    ('count', 'overall frequency'): 'shot types',
    ('forehand (count)', 'forehand ratio (%)'): 'forehand plays',
    ('backhand (count)', 'backhand ratio (%)'): 'backhand plays',
    }

def plot_gender_distribution(df: pd.DataFrame, gender: str, statistic: tuple[str,str]):
    pass

def plot_elite_distribution(sample: pd.DataFrame, statistic: tuple[str, str]) -> tuple[plt.Figure, plt.Axes]:
    """
    View 1: single gender elite distribution of a particular statistic

    Parameters:
        df: Processed DataFrame. Must contain the chosen metric column
            and 'overall frequency' (for annotation).
        gender: 'male' or 'female' – used in the chart title.
        statistic: Tuple of two column names; only the first is used as the metric to plot.
                   Valid metric names: 'count', 'overall frequency', 'forehand (count)',
                   'forehand ratio (%)', 'backhand (count)', 'backhand ratio (%)'

    Returns:
        fig, ax: Matplotlib figure and axes objects.
    """
    metric = statistic[0]
    sample_name = sample[0]
    df = sample[1]  

    df_sorted = df.sort_values(by=metric, ascending=True)

    # Figure and Plot customizations
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(BACKGROUND)   
    ax.set_facecolor(SURFACE)             

    bars = ax.barh(df_sorted.index, df_sorted[metric], **BAR_CUSTOMIZATIONS)
    max_val = df_sorted[metric].max()

    # Annotate each bar with the count and overall frequency percentage
    bars[-1].set_color(SMASH_RED)
    for bar, (idx, row) in zip(bars, df_sorted.iterrows()):
        width = bar.get_width()
        freq_percent = row['overall frequency'] * 100   

        ax.text(
            width + max_val * 0.01,                     
            bar.get_y() + bar.get_height() / 2,
            f'{int(width):,}  ({freq_percent:.1f}%)',
            va='center', ha='left',
            fontsize=8, color=TEXT
        )

    # Styling axes
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['top'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.spines['right'].set_color(GRID)
    ax.grid(axis='x', color=GRID, linestyle='--', linewidth=0.5)

    # Titles and labels
    ax.set_title(f'Distribution of {STAT_LABELS[statistic]} among elite {sample_name} singles players', fontsize=14)
    ax.set_xlabel(metric, fontsize=12)
    ax.set_ylabel('Shot type', fontsize=12)  

    plt.tight_layout()
    plt.show()
    return fig, ax

def plot_comparison(sample_one: tuple[str,pd.DataFrame], sample_two: tuple[str,pd.DataFrame], statistic: tuple[str,str]) -> tuple[plt.Figure, plt.Axes]:
    """
    View 2: Distributions of both elite male and female single players for comparsion of a particular statistic

    Parameters:
        male_df: Processed DataFrame. Must contain the chosen metric column
                 and its relative frequency for (annotation)
        female_df: Processed DataFrame. Must contain the chosen metric column
                   and its relative frequency for (annotation)
        statistic: Tuple of two column names; only the first is used as the metric to plot.
                   Valid metric names: 'count', 'overall frequency', 'forehand (count)',
                   'forehand ratio (%)', 'backhand (count)', 'backhand ratio (%)'
    
    Returns:
        fig, ax: Matplotlib figure and axes objects.
    """

    metric = statistic[0]
    sample_one_name = sample_one[0]
    sample_two_name = sample_two[0]
    df_one_sorted = sample_one[1].sort_values(by=metric, ascending=True)
    df_two_sorted = sample_two[1].sort_values(by=metric, ascending= True)

    fig, axes = plt.subplots(2,1, figsize= (12,10))
    fig.patch.set_facecolor(BACKGROUND)

    def _draw_subplot(ax: plt.axes, df_sorted: pd.DataFrame, subtitle: str) -> None:
        ax.set_facecolor(SURFACE)
        bars = ax.barh(df_sorted.index, df_sorted[metric], **BAR_CUSTOMIZATIONS)

        local_max = df_sorted[metric].max()
        bars[-1].set_color(SMASH_RED)
        for bar, (idx, row) in zip(bars, df_sorted.iterrows()):
            width = bar.get_width()
            freq_percent = row['overall frequency'] * 100

            ax.text(
                width + local_max * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f'{int(width):,}  ({freq_percent:.1f}%)',
                va='center', ha='left',
                fontsize=8, color=TEXT
            )

        ax.tick_params(colors=TEXT, labelsize=9)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_color(GRID)
        ax.grid(axis='x', color=GRID, linestyle='--', linewidth=0.5)
        ax.set_title(subtitle, fontsize=12)
        ax.set_ylabel('Shot type', fontsize=11)

    _draw_subplot(axes[0], df_one_sorted, sample_one_name)
    _draw_subplot(axes[1], df_two_sorted, sample_two_name)

    axes[1].set_xlabel(metric, fontsize=12)
    fig.suptitle(f'Distribution of {STAT_LABELS[statistic]}: {sample_one_name} vs {sample_two_name} singles players', fontsize=14, color=TEXT)

    plt.tight_layout()
    plt.show()
    return fig, axes

# To Be Continued in the Future
def plot_personal_vs_elite(personal_df: pd.DataFrame, elite_df: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    pass


# Main Code
prompt_sample = (
    "\nWhich group of professional singles players would you like to analyze?\n"
    "1: Male winners\n"
    "2: Male losers\n"
    "3: Female winners\n"
    "4: Female losers\n"
)

prompt_statistic = (
    "\nWhich statistic would you like to analyze?\n"
    "1: Overall shot count and frequency\n"
    "2: Forehand count and ratio\n"
    "3: Backhand count and ratio\n"
)

prompt_distribution = (
    "\nWhich distribution would you like to plot?\n"
    "1: Shot distributions by individual elite player\n"
    "2: Shot distributions compared by gender and winning status\n"
    "3: Personal shot distribution vs. elite players (coming soon)\n"
)

statistic = input(f'{prompt_statistic}Enter Choice: ')
match statistic:
    case '1':
        statistic = ('count', 'overall frequency')
    case '2':
        statistic = ('forehand (count)', 'forehand ratio (%)')
    case '3':
        statistic = ('backhand (count)', 'backhand ratio (%)')
    case _:
        raise ValueError(f'Invalid Option')

sample_df = input(f'{prompt_sample}Enter Choice: ')
match sample_df:
    case '1':
        sample_df = ('male (win)', male_win_df)
    case '2':
        sample_df = ('male (lose)', male_lose_df)
    case '3':
        sample_df = ('female (win)', female_win_df)
    case '4':
        sample_df = ('female (lose)', female_lose_df)
    case _:
        raise ValueError("Invalid Option")


distribution = input(f'{prompt_distribution}Enter Choice: ')

match distribution:
    case '1':
        plot_elite_distribution(sample_df, statistic)
    case '2':
        sample_one_df = sample_df
        sample_two_df = input(f'{prompt_sample}Enter Second Sample: ')

        match sample_two_df:
            case '1':
                sample_two_df = ('male (win)', male_win_df)
            case '2':
                sample_two_df = ('male (lose)', male_lose_df)
            case '3':
                sample_two_df = ('female (win)', female_win_df)
            case '4':
                sample_two_df = ('female (lose)', female_lose_df)
            case _:
                raise ValueError("Invalid Option")

        plot_comparison(sample_one_df,sample_two_df,statistic)
    case '3':
        print('functionality currently unavailable')