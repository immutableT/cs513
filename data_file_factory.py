from data_file import DataFile


def create_data_frames():
    dish = DataFile(
        name='Dish',
        col_cant_have_null_values=['id'],
        non_required_col=[
            'description',
            'menus_appeared',
            'times_appeared',
            'first_appeared',
            'last_appeared',
            'lowest_price',
            'highest_price',
        ],
        col_to_coerce_to_int64=['id'],
    )

    menu_item = DataFile(
        name='MenuItem',
        col_cant_have_null_values=['id', 'price', 'menu_page_id', 'dish_id'],
        non_required_col=[
            'updated_at',
            'xpos',
            'ypos',
            'high_price',
            'created_at',
        ],
        col_to_coerce_to_int64=[
            'id',
            'dish_id',
            'menu_page_id',
        ],
    )

    menu = DataFile(
        name='Menu',
        col_cant_have_null_values=['date'],
        non_required_col=[
            'name',
            'sponsor',
            'event',
            'venue',
            'place',
            'physical_description',
            'occasion',
            'notes',
            'call_number',
            'keywords',
            'language',
            'location',
            'location_type',
            'currency',
            'currency_symbol',
            'status',
            'page_count',
            'dish_count',
        ],
        col_to_coerce_to_int64=[
            'id',
        ],
        col_to_coerce_to_datetime=['date']
    )

    menu_page = DataFile(
        name='MenuPage',
        col_cant_have_null_values=['menu_id'],
        non_required_col=[
            'page_number',
            'image_id',
            'full_height',
            'full_width',
            'uuid',
        ],
        col_to_coerce_to_int64=[
            'id',
            'menu_id',
        ],
    )

    dish.clean()
    menu_item.clean()
    menu_page.clean()
    menu.clean()

    return dish.df, menu_item.df, menu_page.df, menu.df
