import os
import cpi
import datetime

from data_file_factory import create_data_frames
from joiner import Joiner


def pre_process():
    dish_df, menu_item_df, menu_page_df, menu_df = create_data_frames()

    joiner = Joiner(
        dish_df=dish_df,
        menu_item_df=menu_item_df,
        menu_page_df=menu_page_df,
        menu_df=menu_df)
    joiner.join()
    full_join_df = joiner.full_join_df

    # CPI package does not go back as far as the NYPL-Menu.
    full_join_df = full_join_df[full_join_df['date'] >= datetime.datetime(1920, 1, 1)]

    full_join_df['adjusted_to_inflation_price'] = full_join_df.apply(
        lambda row: cpi.inflate(row.price, row.date),
        axis=1)

    full_join_df.to_csv(os.path.join('data', 'FullJoin.csv'), index=False)
    print(full_join_df.head())


if __name__ == '__main__':
    # cpi.update()
    pre_process()



