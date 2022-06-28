from enum import Enum
from numpyencoder import NumpyEncoder
import json
import os
import pandas as pd

DATAFRAME_ANALYSIS_KEYS = frozenset([
    'metadata',
    'statistics',
    'insights',
    'suggestions',
])
VARIABLE_DIR = '.variables'


class VariableType(str, Enum):
    DATAFRAME = 'dataframe'
    DATAFRAME_ANALYSIS = 'dataframe_analysis'


class Variable:
    def __init__(self, uuid, pipeline_path, block_uuid, variable_type=None):
        self.uuid = uuid
        self.pipeline_path = pipeline_path
        self.block_uuid = block_uuid
        self.variable_dir_path = os.path.join(pipeline_path, VARIABLE_DIR, block_uuid)
        if not os.path.exists(self.variable_dir_path):
            os.makedirs(self.variable_dir_path)
        self.variable_type = variable_type

    def write_data(self, data):
        if self.variable_type is None and type(data) is pd.DataFrame:
            self.variable_type = VariableType.DATAFRAME
        if self.variable_type == VariableType.DATAFRAME:
            self.__write_parquet(data)
        elif self.variable_type == VariableType.DATAFRAME_ANALYSIS:
            self.__write_dataframe_analysis(data)
        else:
            self.__write_json(data)

    def read_data(self):
        if self.variable_type is None and \
            os.path.exists(
                os.path.join(self.variable_dir_path, f'{self.uuid}', 'data.parquet')):
            # If parquet file exists for given variable, set the variable type to DATAFRAME
            self.variable_type = VariableType.DATAFRAME

        if self.variable_type == VariableType.DATAFRAME:
            return self.__read_parquet()
        elif self.variable_type == VariableType.DATAFRAME_ANALYSIS:
            return self.__read_dataframe_analysis()
        return self.__read_json()

    def __read_json(self, default_value={}):
        file_path = os.path.join(self.variable_dir_path, f'{self.uuid}.json')
        return self.__read_json_file(file_path, default_value)

    def __write_json(self, data):
        if not os.path.isdir(self.variable_dir_path):
            os.mkdir(self.variable_dir_path)
        self.__write_json_file(os.path.join(self.variable_dir_path, f'{self.uuid}.json'), data)

    def __read_json_file(self, file_path, default_value={}):
        if not os.path.exists(file_path):
            return default_value
        with open(file_path) as file:
            return json.load(file)

    def __write_json_file(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, cls=NumpyEncoder)

    def __read_parquet(self):
        variable_path = os.path.join(self.variable_dir_path, f'{self.uuid}')
        file_path = os.path.join(variable_path, 'data.parquet')
        if not os.path.exists(file_path):
            return pd.DataFrame()
        return pd.read_parquet(file_path, engine='pyarrow')

    def __write_parquet(self, data):
        df_output = data.copy()
        # Clean up data types since parquet doesn't support mixed data types
        for c in df_output.columns:
            series_non_null = df_output[c].dropna()
            if len(series_non_null) > 0:
                coltype = type(series_non_null.iloc[0])
                try:
                    df_output[c] = series_non_null.astype(coltype)
                except Exception:
                    # Fall back to convert to string
                    df_output[c] = series_non_null.astype(str)
        variable_path = os.path.join(self.variable_dir_path, f'{self.uuid}')
        os.makedirs(variable_path, exist_ok=True)
        df_output.to_parquet(os.path.join(variable_path, 'data.parquet'))

    def __read_dataframe_analysis(self):
        """
        Read the following files
        1. metadata.json
        2. statistics.json
        3. insights.json
        4. suggestions.json
        """
        variable_path = os.path.join(self.variable_dir_path, f'{self.uuid}')
        if not os.path.exists(variable_path):
            return dict()
        result = dict()
        for k in DATAFRAME_ANALYSIS_KEYS:
            result[k] = self.__read_json_file(os.path.join(variable_path, f'{k}.json'))
        return result

    def __write_dataframe_analysis(self, data):
        """
        Write the following files
        1. metadata.json
        2. statistics.json
        3. insights.json
        4. suggestions.json
        """
        variable_path = os.path.join(self.variable_dir_path, f'{self.uuid}')
        os.makedirs(variable_path, exist_ok=True)
        for k in DATAFRAME_ANALYSIS_KEYS:
            self.__write_json_file(os.path.join(variable_path, f'{k}.json'), data.get(k))