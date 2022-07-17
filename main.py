import os.path
import pandas as pd
import cpi
import zipfile


def clean_file(
        file_name: str,
        drop_col_if_null: list[str],
        drop_not_required_col: list[str],
        convert_to_type: dict[str, str],
        coerce_to_datetime: list[str]):
    """
    Performs basic cleaning task: (1) drops raws with null values, when such raws are required
    for our use-case, (2) drops columns that are not required for our use-case and (3) converts
    columns to the expected type.
    param coerce_to_datetime: List of columns to coerce the type to datetime.
    param file_name: Path to the zip file containing the data (without the .zip extension).
    param drop_col_if_null: List of columns required for the use-case.
    param drop_not_required_col: List of columns not required for the use-case.
    param convert_to_type: List of columns where the data type needs to be coerced.
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


def clean():
    clean_file(
        file_name='MenuItem',
        drop_col_if_null=['price', 'menu_page_id', 'dish_id'],
        drop_not_required_col=['updated_at', 'xpos', 'ypos', 'high_price', 'created_at'],
        convert_to_type={'dish_id': 'int64'},
        coerce_to_datetime=[],
    )

    clean_file(
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
        convert_to_type={},
        coerce_to_datetime=['date']
    )


if __name__ == '__main__':
    # cpi.update()
    clean()



