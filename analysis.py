from load_files import load_sample, load_personal_sample
import pandas as pd

test_df = load_sample('male_win')
personal_df = load_personal_sample()

print(test_df)