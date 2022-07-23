import os

import pandas as pd
import cpi
import datetime

from data_file_factory import create_data_frames


def merge_dishes_to_menu_items(dish_df, menu_item_df):
    join_df = pd.merge(
        left=dish_df,
        right=menu_item_df,
        left_on='id',
        right_on='dish_id',
        how='inner',
        suffixes=('_dish', '_menu_item'))
    join_df.drop(['id_dish'], axis=1, inplace=True)
    join_df['dish_id'] = join_df['dish_id'].astype(
        dtype='int64',
        errors='raise')
    join_df.rename(
        columns={'id_menu_item': 'menu_item_id'},
        inplace=True)
    return join_df


def merge_dishes_to_menu_items_to_menu_page(merge_dishes_to_menu_items_df, menu_page_df):
    join_df = pd.merge(
        left=merge_dishes_to_menu_items_df,
        right=menu_page_df,
        left_on='menu_page_id',
        right_on='id',
        how='inner',
    )
    join_df.drop(['id'], axis=1, inplace=True)
    return join_df


def merge_dishes_to_menu_items_to_menu_page_to_menu(dishes_to_menu_items_to_menu_page, menu_df):
    join_df = pd.merge(
        left=dishes_to_menu_items_to_menu_page,
        right=menu_df,
        left_on='menu_id',
        right_on='id',
        how='inner',
    )

    join_df['year'] = join_df['date'].dt.year
    join_df.drop(['id'], axis=1, inplace=True)
    join_df.sort_values(by=['dish_id', 'year'], ascending=True, inplace=True)
    return join_df


def pre_process():
    dish_df, menu_item_df, menu_page_df, menu_df = create_data_frames()

    dish_to_menu_item_df = merge_dishes_to_menu_items(
        dish_df,
        menu_item_df)
    dish_to_menu_item_to_menu_page_df = merge_dishes_to_menu_items_to_menu_page(
        dish_to_menu_item_df,
        menu_page_df)
    full_join_df = merge_dishes_to_menu_items_to_menu_page_to_menu(
        dish_to_menu_item_to_menu_page_df,
        menu_df)

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



