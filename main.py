import os

from currency_filter import CurrencyFilter
from data_file_factory import create_data_frames
from joiner import Joiner
from inflation_adjuster import InflationAdjuster
from grouper import Grouper


# @BEGIN pre_process
# @IN dish_df @URI file:./data/Dish.zip
# @IN menu_item_df @URI file:./data/MenuItem.zip
# @IN menu_page_df @URI file:./data/MenuPage.zip
# @IN menu_df @URI file:./data/Menu.zip
# @OUT FullJoin.csv @URI file:./data/FullJoin.csv

def pre_process():

    # @BEGIN _coerce_to_int64
    # @IN dish_df @IN menu_item_df @IN menu_page_df @IN menu_df
    # @OUT int_dish_df @OUT int_menu_item_df @OUT int_menu_page_df @OUT int_menu_df
    # @END _coerce_to_int64

    # @BEGIN _coerce_to_datetime
    # @IN int_dish_df @IN int_menu_item_df @IN int_menu_page_df @IN int_menu_df
    # @OUT datetime_dish_df @OUT datetime_menu_item_df @OUT datetime_menu_page_df @OUT datetime_menu_df
    # @END _coerce_to_datetime

    # @BEGIN _drop_non_required_col
    # @IN datetime_dish_df @IN datetime_menu_item_df @IN datetime_menu_page_df @IN datetime_menu_df
    # @OUT drop_dish_df @OUT drop_menu_item_df @OUT drop_menu_page_df @OUT drop_menu_df
    # @END _drop_non_required_col

    # @BEGIN _delete_rows_with_null_values
    # @IN drop_dish_df @IN drop_menu_item_df @IN drop_menu_page_df @IN drop_menu_df
    # @OUT clean_dish_df @OUT clean_menu_item_df @OUT clean_menu_page_df @OUT clean_menu_df
    # @END _delete_rows_with_null_values

    dish, menu_item, menu_page, menu = create_data_frames()
    currency_filter = CurrencyFilter(menu.df)
    currency_filter.clean()
    menu_df = currency_filter.df

    assert sum(dish.df.isnull().values.ravel()) == 0
    assert sum(menu_item.df.isnull().values.ravel()) == 0
    assert sum(menu_page.df.isnull().values.ravel()) == 0
    assert sum(menu_df.isnull().values.ravel()) == 0

    # @BEGIN join
    # @IN clean_dish_df @IN clean_menu_item_df @IN clean_menu_page_df @IN clean_menu_df
    # @OUT full_join_df
    joiner = Joiner(
        dish_df=dish.df,
        menu_item_df=menu_item.df,
        menu_page_df=menu_page.df,
        menu_df=menu_df)
    joiner.join()
    full_join_df = joiner.full_join_df
    # @END Join

    # @BEGIN inflation_adjuster
    # @IN full_join_df
    # @OUT inflation_adjuster.adjusted_df @AS inflation_adjusted_df
    inflation_adjuster = InflationAdjuster(full_join_df=full_join_df)
    inflation_adjuster.inflate()
    # @END inflation_adjuster

    # TODO: Remove rows where price is greater than 100.

    # @BEGIN grouping
    # @IN inflation_adjuster.adjusted_df @AS inflation_adjusted_df
    # @OUT FullJoin.csv @URI file:./data/FullJoin.csv
    grouper = Grouper(inflation_adjuster.adjusted_df)
    grouper.group()

    grouper.df.to_csv(
        os.path.join('data', 'FullJoin.csv'),
        index=False)
    print(inflation_adjuster.adjusted_df.head())
    # @END grouping

# @END pre_process


if __name__ == '__main__':
    # cpi.update()
    pre_process()
