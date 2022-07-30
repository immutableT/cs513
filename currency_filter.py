import pandas as pd

currencies_to_ignore = [
    'Francs',
    'Belgian Francs',
    'Shillings',
    'Deutsche Marks',
    'UK Pounds',
    'Pence',
    'Canadian Dollars',
    'Austro-Hungarian Kronen',
    'Swiss Francs',
    'Pesetas',
    'Danish kroner'
    'Swedish kronor (SEK/kr)',
    'Escudos',
    'Yen',
    'Italian Lire',
    'Mexican pesos',
    'Quetzales',
    'Israeli lirot (1948-1980)',
    'Monégasque francs',
    'Qatari riyal',
    'Dutch Guilders',
    'Austrian Schillings',
    'Euros',
    'Norwegian kroner',
    'Moroccan Dirham',
    'Bermudian dollars',
    'Hungarian forint',
    'Drachmas',
    'New Taiwan Dollar',
    'Icelandic Krónur',
    'Australian Dollars',
    'Argentine peso',
    'Sol',
    'Uruguayan pesos',
    'Brazilian Cruzeiros',
    'Złoty',
    'Cuban pesos',
    'Finnish markka',
    'Lats'
    'Straits dollar (1904-1939)',
]


class CurrencyFilter:
    def __init__(self, df:pd.DataFrame):
        self._df = df

    @property
    def df(self):
        return self._df

    def clean(self):
        print(f'Number of menus before filtering by currency {len(self._df)}')
        self._df = self._df[~self._df['currency'].isin(currencies_to_ignore)]
        self._df.drop(['currency'], axis=1, inplace=True)
        print(f'Number of menus after filtering by currency {len(self._df)}')

