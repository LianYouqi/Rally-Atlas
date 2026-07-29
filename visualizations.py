import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# [[[Data and Statistics]]]
male_df   = pd.read_csv('processed_data/Badminton Shot Distribution (Male)',   index_col='shot type')
male_shot_types = male_df.index
# male_shot_count = male_df['count'].sort_values(ascending=True)
# male_overall_freq = male_df['overall frequency'].sort_values(ascending=True)
# male_forehand_count = male_df['forehand (count)'].sort_values(ascending=True)
# male_forehand_ratio = male_df['forehand ratio (%)'].sort_values(ascending=True)
# male_backhand_count = male_df['backhand (count)'].sort_values(ascending=True)
# male_backhand_ratio = male_df['backhand ratio (%)'].sort_values(ascending=True)

female_df = pd.read_csv('processed_data/Badminton Shot Distribution (Female)', index_col='shot type')
female_shot_types = female_df.index
# female_shot_count = female_df['count'].sort_values(ascending=True)
# female_overall_freq = female_df['overall frequency'].sort_values(ascending=True)
# female_forehand_count = female_df['forehand (count)'].sort_values(ascending=True)
# female_forehand_ratio = female_df['forehand ratio (%)'].sort_values(ascending=True)
# female_backhand_count = female_df['backhand (count)'].sort_values(ascending=True)
# female_backhand_ratio = female_df['backhand ratio (%)'].sort_values(ascending=True)

# ── Palette ───────────────────────────────────────────────────────────────────
COURT_TEAL  = '#1B998B'
SMASH_RED   = '#E84855'
BACKGROUND  = '#0F1923'   # dark court-floor tone
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

AXIS_CUSTOMIZATIONS = {

}
# # Prototype
# plt.barh(male_shot_count.index, male_shot_count,**BAR_CUSTOMIZATIONS)
# plt.tight_layout()
# plt.xlabel('Total Shots')
# plt.ylabel('Shot Type')
# plt.show()

def plot_elite_distribution(df: pd.DataFrame, gender: str, statistic: tuple[str,str]) -> tuple[plt.Figure, plt.Axes]:
    """View 1: single gender elite distribution
    
    Parameters:
        df: Processed DataFrame from processing.py.
            Must contain columns 'count', 'overall frequency', 'forehand (count)',
            'forehand ratio (%)', 'backhand (count)', 'backhand ratio (%)'
        gender: Used to label the chart title. 
                Valid input are 'male' and 'female'
        statistic: Column name determing which metric to plot.
                   Valid values: 'count', 'overall frequency', 'forehand (count)',
                   'forehand ratio (%)', 'backhand (count)', 'backhand ratio (%)'
    Returns:
        None
    """

    figure, axes = plt.subplot(2,1)
    #Top Plot

    #Bottom Plot
    plt.tight_layout()
    plt.show()

def plot_gender_comparison(male_df: pd.DataFrame, female_df: pd.DataFrame, statistics: tuple[str,str]) -> tuple[plt.Figure, plt.Axes]:
    pass

# To Be Continued in the Future
def plot_personal_vs_elite(personal_df: pd.DataFrame, elite_df: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    pass



#Prompts the user to display which kind of statistic to be plotted.
prompt_one = (
    "Which of the following distributions would you like to plot?\n"
    "1. Different shot distributions of elite badminton players.\n"
    "2. Comparison of shot distributions among elite male and female badminton players.\n"
    "3. Personal comparison of shot distribution (To be Continued)\n"
)
prompt_two = (
    "Which of the following statistics would you like to analyze?\n"
    "1. Shot Count / Overall Frequency\n"
    "2. Forehand Count / Forehand Ratio\n"
    "3. Backhand Count / Backhand Ratio\n"
)
prompt_gender = (
    "Which gender?\n" 
    "1. male\n"
    "2. female\n"
)

which_distribution = input(f'{prompt_one}Enter Choice: ')
statistic = input(f'{prompt_two}Enter Choice:')
gender = input(f'{prompt_gender}Enter Choice: ')

match gender:
    case '1':
        gender = 'male'
    case '2':
        gender = 'female'
    case _:
        raise ValueError('Data is only available for the following genders: male and female')

match statistic:
    case '1':
        statistic = ('count', 'overall frequency')
    case '2':
        statistic = ('forehand (count)', 'forehand ratio (%)')
    case '3':
        statistic = ('backhand (count)', 'backhand ratio (%)')

match which_distribution:
    case '1':
        df = male_df if gender == 'male' else female_df

        plot_elite_distribution(df, gender, statistic)

    case '2':
        # plot_gender_comparison(male_df, female_df, statistic)

    case '3':
        # plot_personal_vs_elite()
        pass