"""Demo Module definition file"""
from .module import ToniqEnvManager

class DataManager(ToniqEnvManager):
  """Demo Module class to run in a Toniq Notebook"""
  def __init__(self, provider='gcp'):
    ToniqEnvManager.__init__(self, provider=provider)

    # init spark
    self.spark = self.store.init_spark()

    # get data grops from toniq store
    self.data_groups = self.tq.get_data_groups()

    # default the storage data_group
    self.data_group_id = self.data_groups.storage_data_group[0].id

  def write_toniq_table(self, df , table_name, verbose = True):
    """
    Writes csv to toniq datastore

    params:

        df: pandas dataframe
        table_name: name of table being written to Toniq Data Store
        verbose: verbose indicator for saving dataframe

    """

    # convert panadas df to spark df
    spark_df = self.spark.createDataFrame(df)

    # write spark df to
    self.store.write_table(spark_df, self.data_group_id, table_name)

    if verbose:
      print(f"Saved Toniq Table ({table_name})")

  def load_toniq_table(self, table_name : str, sql_tempview: bool = True):
    """
    Simple demo function that loads a table (of patient information)
    and runs a SQL query to aggregate statistics

    params:

        table_name : name of table being loading from Toniq Store
        sql_tempview: include the spark dataframe as a temp table

    returns:
        loaded_df: Spark dataframe

    """

    loaded_df = self.store.load_table(self.data_group_id, table_name)
    # query the table is the string is provided
    if sql_tempview:
      loaded_df.createOrReplaceTempView(table_name)
    return loaded_df
