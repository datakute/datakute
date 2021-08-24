import mysql.connector
from mysql.connector import Error
from config.config import Config
from common.logger_conf import logger
from sqlalchemy import create_engine

class MySqlConnector:
    def __init__(self,file):
        self._config = Config(file)
        self._engine()

# Intialize MySQL
    def conn(self):
        try:
            self.connection = mysql.connector.connect(host=self._config.HOST,
                                                 database=self._config.DB,
                                                 user=self._config.USER,
                                                 password=self._config.PASSWORD)
            if connection.is_connected():
                db_info = connection.get_server_info()
                logger.info(f"Connected to MySQL Server version {db_info}")
                return connection        
        except Error as e:
            logger.info("Error while connecting to MySQL", e)

    def _engine(self):
        connection_string = f"mysql+pymysql://{self._config.USER}:{self._config.PASSWORD}@{self._config.HOST}/{self._config.DB}"
        try:
            self._connection = create_engine(connection_string)
        except Error as e:
            logger.info("Error while connecting to MySQL", e)


    def _drop_table(self, table_name):
        self.__execute(f"DROP TABLE IF EXISTS {table_name}")
        
    def _create_data_tracker_table(self, table_name):
        self._drop_table(table_name)
        create_statement = f""" create table {table_name} \
        (time timestamp not null, 
         sensor_name varchar(200) not null, 
         value long not null, 
         primary key(time, sensor_name))"""
        self.__execute(create_statement)

    def _insert_data_df(self, table, df):
        df.to_sql(table, self._connection, index=False, if_exists="append")
   
    def __execute(self, statement):
        return self._connection.execute(statement)
