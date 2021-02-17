import matplotlib
import pandas as pd

CSV_FILE = 'data.csv'


class DataProcessing:

    def __init__(self):
        self.df = pd.read_csv(CSV_FILE, parse_dates=['Data'])
        self.last_date = self.df['Data'].max().date()
        self.today = pd.Timestamp.today().date()
        self._columns = self.df.columns

    def update(self, data: list) -> None:
        new_df = pd.DataFrame(data, columns=self._columns)
        new_df['Data'] = pd.to_datetime(new_df['Data'])
        self.df = self.df.append(new_df).sort_values(['Data'], ascending=False)

    def write_csv(self) -> None:
        self.df.to_csv(CSV_FILE, index=None)

    def __str__(self):
        first_date = self.df['Data'].min().date()
        return f'Records from {first_date} to {self.last_date}'
