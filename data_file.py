import os
import zipfile
from os.path import exists
from typing import Optional
import pandas as pd


class DataFile:
    def __init__(
            self,
            name: str,
            col_cant_have_null_values: list[str],
            non_required_col: list[str],
            col_to_coerce_to_int64: Optional[list[str]] = None,
            col_to_coerce_to_datetime: Optional[list[str]] = None):
        """

        :param name:
        :param col_cant_have_null_values:
        :param non_required_col:
        :param col_to_coerce_to_int64:
        :param col_to_coerce_to_datetime:
        """
        self._name = name
        self._col_cant_have_null_values = col_cant_have_null_values
        self._non_required_col = non_required_col
        if not col_to_coerce_to_int64:
            self._col_to_coerce_to_int64 = []
        else:
            self._col_to_coerce_to_int64 = col_to_coerce_to_int64
        if not col_to_coerce_to_datetime:
            self._col_to_coerce_to_datetime = []
        else:
            self._col_to_coerce_to_datetime = col_to_coerce_to_datetime

        path_to_zip = os.path.join('data', f'{name}.zip')
        if not exists(path_to_zip):
            raise RuntimeError(f'no such file {path_to_zip}')
        with zipfile.ZipFile(path_to_zip, 'r') as zipf:
            zipf.extractall(os.path.join('data'))

        path = os.path.join('data', f'{name}.csv')
        self._df = pd.read_csv(path)

    @property
    def df(self):
        return self._df

    def _coerce_to_int64(self):
        for col in self._col_to_coerce_to_int64:
            try:
                self._df[col] = self._df[col].astype(dtype='int64', errors='raise')
            except pd.errors.IntCastingNaNError:
                self._df[col] = pd.to_numeric(self._df[col], errors='coerce')

    def _coerce_to_datetime(self):
        for col in self._col_to_coerce_to_datetime:
            self._df[col] = pd.to_datetime(self._df[col], errors='coerce')

    def _drop_non_required_col(self):
        self._df.drop(self._non_required_col, axis=1, inplace=True)

    def _delete_rows_with_null_values(self):
        self._df.dropna(subset=self._col_cant_have_null_values, inplace=True)

    def clean(self):
        """
        Implements the process of pre-processing a dirty file.
        """
        # All columns that we expect to be in int64 (ex. id) will be coerced to int64
        self._coerce_to_int64()
        # All columns that we expect to be in datetime (ex. menu.date) will be coerced to datetime.
        self._coerce_to_datetime()
        # To reduce the size of the dataset, remove the columns that are not required for our use-case.
        self._drop_non_required_col()
        # For the columns that are required for our use-case, delete all rows with null values.
        self._delete_rows_with_null_values()

    def save(self):
        save_path = os.path.join('data', f'{self._name}')
        try:
            os.remove(save_path)
        except FileNotFoundError:
            pass
        self._df.to_csv(save_path, index=False)
