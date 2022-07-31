import pandas as pd
import numpy as np


class Grouper:
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._group_level_one = None

    @property
    def df(self):
        return self._group_level_one

    def _group_by_dish_id_and_year(self):
        self._group_level_one = self._df.groupby(
            ['dish_id', 'year'], as_index=False).agg(
                Mean=('adjusted_to_inflation_price', np.mean),
                Std=('adjusted_to_inflation_price', np.std),
        )

    def group(self):
        self._group_by_dish_id_and_year()
        # TODO: Add second level of grouping - by year.


