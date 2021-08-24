import os
import timeit
import pandas as pd
from multiprocessing import Pool, current_process
from common.utils import DataReader
from config.config import Config
from common.logger_conf import logger
from common.utils import TimeSeriesGenerator
from connectors.mysql_connector import MySqlConnector 

class DataCollector:
    def __init__(self, file="/Users/balakrishna.maduru/Documents/my_work/data_tracker/config/data_tracker.yaml"):
        self._config = Config(file)
        self.__reader = DataReader(self._config)
    
    def data_reader_and_process(self):
        pool = Pool(1)
        self.__pre_processing()
        pool.map(self.process_data, self.__reader.get_paths(self._config.Source))

    def process_data(self, path):
        self._process_id = f"{os.getppid()}{os.getpid()}"
        logger.info(f'Started file execution under process id - {self._process_id} and file {path}')
        start = timeit.default_timer()
        self._df = self.__reader._read(path)
        self._get_stats()
        stop = timeit.default_timer()
        logger.info(f'Time taken to execute process - {self._process_id} - {stop - start}')
        
    def _get_stats(self,freq="min"):
        print("Doneee.........")
        grouped = self._df.groupby([pd.Grouper(key=self._config.TimeSeriesColumn, freq=freq), self._config.ItemName])[self._config.AggragationColumn].count().reset_index()
        print(grouped)
        self.__insert_data(grouped)
        
    def __insert_data(self, grouped):
        my_sql = MySqlConnector("/Users/balakrishna.maduru/Documents/my_work/data_tracker/user_configurations/my_sql.yaml")
        my_sql._insert_data_df(self._config.Name, grouped)
        
    def __pre_processing(self):
        my_sql = MySqlConnector("/Users/balakrishna.maduru/Documents/my_work/data_tracker/user_configurations/my_sql.yaml")
        my_sql._create_data_tracker_table(self._config.Name)

        
        
    # def _compare_actual_and_expected(self):
    #     expected_time_series = self._get_expected_records()
    #     actual_record_count = self._df.shape[0]
    #     print(self._df)
    #     number_of_items = self._df["SYMBOL"].nunique()
    #     expected_record_count = number_of_items * len(expected_time_series)
    #     return actual_record_count == expected_record_count
    #
    #
    # def _get_expected_records(self):
    #     min_datetime, max_datetime = self._get_min_max_datetime()
    #     logger.info(f"Min and Max time for - {self._process_id} - {min_datetime} - {max_datetime}")
    #     tsg = TimeSeriesGenerator()
    #     expected_time_series = tsg.generate_time_series_dates_based_on_granularity(min_datetime, max_datetime , "1D")
    #     return expected_time_series

    def _get_min_max_datetime(self):
        return min(self._df[self._config.time_series_column]), max(self._df[self._config.time_series_column])