from data_processor.data_collector import DataCollector
import re
from  datetime import datetime
import pandas as pd




if __name__ == "__main__":
    dc = DataCollector()
    df = dc.data_reader_and_process()
    
