import os

from data_file_factory import create_data_frames
from joiner import Joiner
from inflation_adjuster import InflationAdjuster
from grouper import Grouper


def pre_process():
    dish_df, menu_item_df, menu_page_df, menu_df = create_data_frames()

    joiner = Joiner(
        dish_df=dish_df,
        menu_item_df=menu_item_df,
        menu_page_df=menu_page_df,
        menu_df=menu_df)
    joiner.join()
    full_join_df = joiner.full_join_df

    inflation_adjuster = InflationAdjuster(full_join_df=full_join_df)
    inflation_adjuster.inflate()

    # TODO: Remove rows where price is greater than 100.

    grouper = Grouper(inflation_adjuster.adjusted_df)
    grouper.group()

    grouper.df.to_csv(
        os.path.join('data', 'FullJoin.csv'),
        index=False)
    print(grouper.df.head())


if __name__ == '__main__':
    # cpi.update()
    pre_process()



