

"""Demo Module definition file"""
from module import ToniqEnvManager
import pandas as pd 
import pyspark.sql.functions as f


class DataManager(ToniqEnvManager):
  """Demo Module class to run in a Toniq Notebook"""
  def __init__(self, provider='gcp'):
    ToniqEnvManager.__init__(self, provider=provider)
    # init spark
    self.spark = self.store.init_spark()
    
    
    """
    Toniq Data Store Groups
    """
    self.store_groups= {}
    self.store_group_id = {}
    
    
    for store in ["data", "feature"]:
        # get data grops from toniq store
        self.store_groups[store] = getattr(self.tq, f"get_{store}_groups")()
         # default the storage data_group
        self.store_group_id[store] = getattr(self.store_groups[store], f"storage_{store}_group")[0].id
    
  def list_tables(self, store="data"):
    
    """
    Lists the tables in the specified {store} : ["feature", "data"]
    
    """
    if store == "data":
        self.store.list_tables(self.store_group_id[store])
    elif store == "feature":
        self.store.list_features(self.store_group_id[store])

  def write_table(self,
                  df ,
                  name,
                  store="data",
                  verbose = True,
                  partition=None, save_presto=False):
    """
    Writes csv to toniq datastore

    params:

        df: pandas dataframe
        table_name: name of table being written to Toniq Data Store
        store: feature or data store
        verbose: verbose indicator for saving dataframe
        save_presto:  boolean indicating to save presto table

    """
    
    # convert panadas df to spark df
    if "pandas" in str(type(df)):
        df = self.spark.createDataFrame(df)

    # write spark df to
    if store == "data":
        self.store.write_table(df, self.store_group_id[store], name)
    elif store == "feature":
        self.store.write_feature(df, group_id=self.store_group_id[store], partition=partition, feature_name=name)
    

    if verbose:
        print(f"Saved Toniq Table ({name})")
    
    
    
    if save_presto:
        self.write_presto(df=df, name=name, verbose = verbose)
        
        

  def load_table(self, 
                 name : str,
                 store: str, 
                 partition: str,
                 store_group_id: str= None,
                 sql_tempview: bool = False):
    """
    Simple demo function that loads a table (of patient information)
    and runs a SQL query to aggregate statistics

    params:

        table_name : name of table being loading from Toniq Store
        store: feature or data store
        sql_tempview: include the spark dataframe as a temp table

    returns:
        loaded_df: Spark dataframe

    """
    if store == "data":
        df = self.store.load_table(self.store_group_id[store], name)
    elif store == "feature":
        df = self.store.load_feature(self.store_group_id[store], partition ,name)
    
    
    # query the table is the string is provided
    if sql_tempview:
        df.createOrReplaceTempView(name)
    return df

  
  def write_presto(self, df, name, store,  verbose = False):


      """
      Simple demo function that loads a table (of patient information)
      and runs a SQL query to aggregate statistics

      params:

          df : spark dataframe
          table_name: name of the presto table
          store: data or feature group
          verbose: verbosity

      returns:
          loaded_df: Spark dataframe

      """

      # Infer presto schema from spark dataframe string
      df = df.select(*[f.col(c).alias(c.replace("-", ""))for c in df.columns])
      presto_schema = str(df).lstrip("DataFrame").strip("[]").replace(":", "")


      # drop table if it already exists
      self.cur.execute(f"DROP TABLE IF EXISTS {name}")
      self.cur.fetchall()

      # create the table if it does not already exists
      create_sql = f"""CREATE EXTERNAL TABLE IF NOT EXISTS {name}({presto_schema})"""
      self.store.create_external_table(self.store_group_id[store], name, create_sql) 
    
    
      

      if verbose:
          print(f"Saved {name} into PRESTO")
        
        
  def query_presto(query=""):
    """
    Query PRESTODB
    
    params:
      query: query string
    
    returns:
      pandas dataframe
    
    """
    return pd.read_sql_query(q, self.conn)
    