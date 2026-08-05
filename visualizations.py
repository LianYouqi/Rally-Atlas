import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# [[[Data and Statistics]]]
male_df   = pd.read_csv('processed_data/Badminton Shot Distribution (Male)',   index_col='shot type')
female_df = pd.read_csv('processed_data/Badminton Shot Distribution (Female)', index_col='shot type')
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

def plot_elite_distribution(df: pd.DataFrame, gender: str, statistic: tuple[str, str]) -> tuple[plt.Figure, plt.Axes]:
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
    STAT_LABELS = {
    ('count', 'overall frequency'): 'shot types',
    ('forehand (count)', 'forehand ratio (%)'): 'forehand plays',
    ('backhand (count)', 'backhand ratio (%)'): 'backhand plays',
    }
    metric = statistic[0]  

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
    ax.set_title(f'Distribution of {STAT_LABELS[statistic]} among elite {gender} singles players', fontsize=14)
    ax.set_xlabel(metric, fontsize=12)
    ax.set_ylabel('Shot type', fontsize=12)  

    plt.tight_layout()
    plt.show()
    return fig, ax

def plot_gender_comparison(male_df: pd.DataFrame, female_df: pd.DataFrame, statistic: tuple[str,str]) -> tuple[plt.Figure, plt.Axes]:
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
    STAT_LABELS = {
        ('count', 'overall frequency'): 'shot types',
        ('forehand (count)', 'forehand ratio (%)'): 'forehand plays',
        ('backhand (count)', 'backhand ratio (%)'): 'backhand plays',
        }
    
    metric = statistic[0]
    male_df_sorted = male_df.sort_values(by=metric, ascending=True)
    female_df_sorted = female_df.sort_values(by=metric, ascending= True)

    fig, axes = plt.subplots(2,1, figsize= (12,10))
    fig.patch.set_facecolor(BACKGROUND)

    def _draw_subplot(ax: plt.axes, df_sorted: pd.DataFrame, subtitle: str) -> None:
        ax.set_facecolor(SURFACE)
        bars = ax.barh(df_sorted.index, df_sorted[metric], **BAR_CUSTOMIZATIONS)

        local_max = df_sorted[metric].max()

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

    _draw_subplot(axes[0], male_df_sorted, 'Male')
    _draw_subplot(axes[1], female_df_sorted, 'Female')

    axes[1].set_xlabel(metric, fontsize=12)
    fig.suptitle(f'Distribution of {STAT_LABELS[statistic]}: Male vs Female singles players', fontsize=14, color=TEXT)

    plt.tight_layout()
    plt.show()
    return fig, axes

# To Be Continued in the Future
def plot_personal_vs_elite(personal_df: pd.DataFrame, elite_df: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    pass



#Prompts the user to display which kind of statistic to be plotted.
#[[[CURRENT PROBLEMS:
#   1. THE ORDER IN WHICH THE PROMPTS ARE ASKED ARE IN THE WRONG ORDER ==> DOES NOT WORK IF USER PICKS 3RD OPTION.
#      BETTER STRUCTURE IS REQUIRED WHEN plot_personal_vs_elite FUNCTION IS COMPLETED
#   2. MISSING DEFAULT CASES FOR match 'statistics' AND 'which_distribution']]]

# Statistics - Distribution 
# if User picks second distribution - gender prompt is not nesscary

prompt_one = (
    "Which of the following statistics would you like to analyze?\n"
    "1. Shot Count / Overall Frequency\n"
    "2. Forehand Count / Forehand Ratio\n"
    "3. Backhand Count / Backhand Ratio\n"
)

prompt_two = (
    "Which of the following distributions would you like to plot?\n"
    "1. Different shot distributions of elite badminton players.\n"
    "2. Comparison of shot distributions among elite male and female badminton players.\n"
    "3. Personal comparison of shot distribution (To be Continued)\n"
)

prompt_gender = (
    "Which gender?\n" 
    "1. male\n"
    "2. female\n"
)

statistic = input(f'{prompt_one}Enter Choice:')
which_distribution = input(f'{prompt_two}Enter Choice: ')


match statistic:
    case '1':
        statistic = ('count', 'overall frequency')
    case '2':
        statistic = ('forehand (count)', 'forehand ratio (%)')
    case '3':
        statistic = ('backhand (count)', 'backhand ratio (%)')
    case _:
        raise ValueError(f'Invalid Option')


match which_distribution:
    case '1':
        gender = input(f'{prompt_gender}Enter Choice: ')
        if gender == '1':
            gender = 'male'
            df = male_df
        elif gender == '2':
            gender = 'female'
            df = female_df
        else:
            raise ValueError('Data is only available for the following genders: male and female')
        plot_elite_distribution(df, gender, statistic)
    case '2':
        plot_gender_comparison(male_df, female_df, statistic)

    case '3':
        gender = input(f'{prompt_gender}Enter Choice: ')
        if gender == '1':
            gender = 'male'
            df = male_df
        elif gender == '2':
            gender = 'female'
            df = female_df
        else:
            raise ValueError('Data is only available for the following genders: male and female')
        plot_personal_vs_elite()

    case _:
        raise ValueError(f'Invalid Option')