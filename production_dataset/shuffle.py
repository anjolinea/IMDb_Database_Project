import pandas as pd
from prod_dataset_consts import *

for filename in ALL_FILENAMES:
    df = pd.read_csv(filename)
    df = df.sample(frac = 1)
    df.to_csv(filename, index=False)