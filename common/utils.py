import fsspec
import pandas as pd
from common.logger_conf import logger


class DataReader:
    def __init__(self, config):
        self.__fs = fsspec.filesystem('file')
        self._config = config

    def get_paths(self, path):
        return self.__fs.glob(f'{path}/*')

    def _read(self, path):
        df = pd.read_csv(path)
        df[self._config.TimeSeriesColumn] = pd.to_datetime(df[self._config.TimeSeriesColumn])
        return df


class TimeSeriesGenerator:
    def __init__(self):
        pass
    
    def generate_time_series_dates_based_on_granularity(self, start, end, intervel):
        return pd.date_range(start=start, end=end, freq=intervel)



# if __name__ == "__main__":
#     config = {'source': '/Users/balakrishna.maduru/Documents/my_work/data_tracker/Data/', 'sort_keys': ['TIME']}
#
#     reader = DataReader(config)
#     path_list = reader.get_paths()
#     df = reader.get_data(path_list)
#     print(df)
