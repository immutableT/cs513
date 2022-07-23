from datetime import datetime
import cpi

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


class InflationAdjuster:
    def __init__(self, full_join_df):
        self._full_join_df = full_join_df
        self._adjusted_df = None

    @property
    def adjusted_df(self):
        return self._adjusted_df

    def inflate(self):
        # CPI package does not go back as far as the NYPL-Menu.
        self._adjusted_df = self._full_join_df[self._full_join_df['date'] >= datetime(1920, 1, 1)]

        self._adjusted_df['adjusted_to_inflation_price'] = self._adjusted_df.apply(
            lambda row: cpi.inflate(row.price, row.date),
            axis=1)
