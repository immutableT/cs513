import pandas as pd


class Joiner:
    def __init__(self, dish_df, menu_item_df, menu_page_df, menu_df):
        self._dish_df = dish_df
        self._menu_item_df = menu_item_df
        self._menu_page_df = menu_page_df
        self._menu_df = menu_df
        self._dishes_to_menu_items = None
        self._dishes_to_menu_items_to_menu_page_df = None
        self._full_join_df = None

    @property
    def full_join_df(self):
        return self._full_join_df

    def _join_dishes_to_menu_items(self):
        self._dishes_to_menu_items_df = pd.merge(
            left=self._dish_df,
            right=self._menu_item_df,
            left_on='id',
            right_on='dish_id',
            how='inner',
            suffixes=('_dish', '_menu_item'))
        self._dishes_to_menu_items_df.drop(['id_dish'], axis=1, inplace=True)
        self._dishes_to_menu_items_df['dish_id'] = self._dishes_to_menu_items_df['dish_id'].astype(
            dtype='int64',
            errors='raise')
        self._dishes_to_menu_items_df.rename(
            columns={'id_menu_item': 'menu_item_id'},
            inplace=True,
        )

    def _join_dishes_to_menu_items_to_menu_page(self):
        self._dishes_to_menu_items_to_menu_page_df = pd.merge(
            left=self._dishes_to_menu_items_df,
            right=self._menu_page_df,
            left_on='menu_page_id',
            right_on='id',
            how='inner',
        )
        self._dishes_to_menu_items_to_menu_page_df.drop(['id'], axis=1, inplace=True)

    def _join_dishes_to_menu_items_to_menu_page_to_menu(self):
        self._full_join_df = pd.merge(
            left=self._dishes_to_menu_items_to_menu_page_df,
            right=self._menu_df,
            left_on='menu_id',
            right_on='id',
            how='inner',
        )

        self._full_join_df['year'] = self._full_join_df['date'].dt.year
        self._full_join_df.drop(['id'], axis=1, inplace=True)
        self._full_join_df.sort_values(by=['dish_id', 'year'], ascending=True, inplace=True)

    def join(self):
        self._join_dishes_to_menu_items()
        self._join_dishes_to_menu_items_to_menu_page()
        self._join_dishes_to_menu_items_to_menu_page_to_menu()




