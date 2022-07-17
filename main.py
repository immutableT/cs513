import os.path
import pandas as pd
import cpi
import zipfile


def clean_file(
        file_name: str,
        drop_col_if_null: list[str],
        drop_not_required_col: list[str],
        convert_to_type: dict[str, str] = {},
        coerce_to_datetime: list[str] = []) -> pd.DataFrame:
    """
    Performs basic cleaning task: (1) drops raws with null values, when such raws are required
    for our use-case, (2) drops columns that are not required for our use-case and (3) converts
    columns to the expected type.
    param coerce_to_datetime: List of columns to coerce the type to datetime.
    param file_name: Path to the zip file containing the data (without the .zip extension).
    param drop_col_if_null: List of columns required for the use-case.
    param drop_not_required_col: List of columns not required for the use-case.
    param convert_to_type: List of columns where the data type needs to be coerced.
    return: DataFrame with clean data.
    """
    path_to_zip = os.path.join('data', f'{file_name}.zip')
    with zipfile.ZipFile(path_to_zip, 'r') as zipf:
        zipf.extractall(os.path.join('data'))

    path = os.path.join('data', f'{file_name}.csv')
    df = pd.read_csv(path)
    df.dropna(subset=drop_col_if_null, inplace=True)
    df.drop(drop_not_required_col, axis=1, inplace=True)

    df = df.astype(convert_to_type, errors='raise')
    for col in coerce_to_datetime:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # At this point, we should not have any null values.
    df.dropna(inplace=True)

    save_path = os.path.join('data', f'{file_name}.csv')
    try:
        os.remove(save_path)
    except FileNotFoundError:
        pass

    df.to_csv(save_path, index=False)
    return df


def clean():
    menu_item_df = clean_file(
        file_name='Dish',
        drop_col_if_null=['id'],
        drop_not_required_col=[
            'description',
            'menus_appeared',
            'times_appeared',
            'first_appeared',
            'last_appeared',
            'lowest_price',
            'highest_price',
        ],
        convert_to_type={'id': 'int64'},
    )

    menu_item_df = clean_file(
        file_name='MenuItem',
        drop_col_if_null=['price', 'menu_page_id', 'dish_id'],
        drop_not_required_col=['updated_at', 'xpos', 'ypos', 'high_price', 'created_at'],
        convert_to_type={'dish_id': 'int64'},
    )

    menu_df = clean_file(
        file_name='Menu',
        drop_col_if_null=['date'],
        drop_not_required_col=[
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
        coerce_to_datetime=['date']
    )

    menu_page_df = clean_file(
        file_name='MenuPage',
        drop_col_if_null=['menu_id'],
        drop_not_required_col=[
            'page_number',
            'image_id',
            'full_height',
            'full_width',
            'uuid',
        ],
        convert_to_type={'id': 'int64', 'menu_id': 'int64'},
    )


if __name__ == '__main__':
    # cpi.update()
    clean()



