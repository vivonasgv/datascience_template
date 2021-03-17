"""Demo Module definition file"""

import pandas as pd
from .module import ToniqEnvManager

class DemoModule(ToniqEnvManager):
  """Demo Module class to run in a Toniq Notebook"""
  def __init__(self, provider='gcp'):
    ToniqEnvManager.__init__(self, provider=provider)
    self.spark = self.store.init_spark()
    self.data_groups = self.tq.get_data_groups()
    self.data_group_id = self.data_groups.storage_data_group[0].id
    self.table_name = 'demo_patients_feb_2020'
    self.county_df = None
    self.county_extarnal_df = None

  def write_patients(self):
    """
    Simple demo function that writes a table (of patient information)
    """
    patients = pd.read_csv('./data/raw/patients.csv')
    patients_df = self.spark.createDataFrame(patients)
    self.store.write_table(patients_df, self.data_group_id, self.table_name)

  def run_patients(self):
    """
    Simple demo function that loads a table (of patient information)
    and runs a SQL query to aggregate statistics
    """
    loaded_patients_df = self.store.load_table(self.data_group_id, self.table_name)
    loaded_patients_df.createOrReplaceTempView('raw_patients')

    df = self.spark.sql('''
    SELECT COUNTY, COUNT(*) as COUNT FROM raw_patients
    GROUP BY COUNTY
    ORDER BY COUNT DESC
    ''')
    self.county_df = df.toPandas()

  def run_patients_external_table(self):
    """
    Simple demo function that loads an external table (of patient
    information) and runs a SQL query to aggregate statistics
    """
    create_sql = '''
    CREATE EXTERNAL TABLE IF NOT EXISTS raw_patients(
      Id string,
      BIRTHDATE string,
      DEATHDATE string,
      SSN string,
      DRIVERS string,
      PASSPORT string,
      PREFIX string,
      FIRST string,
      LAST string,
      SUFFIX string,
      MAIDEN string,
      MARITAL string,
      RACE string,
      ETHNICITY string,
      GENDER string,
      BIRTHPLACE string,
      ADDRESS string,
      CITY string,
      STATE string,
      COUNTY string,
      ZIP string,
      LAT float,
      LON float,
      HEALTHCARE_EXPENSES float,
      HEALTHCARE_COVERAGE float
    )
    '''
    self.store.create_external_table(self.data_group_id, self.table_name, create_sql)

    self.cur.execute('''
    SELECT COUNTY, COUNT(*) as COUNT FROM raw_patients
    GROUP BY COUNTY
    ORDER BY COUNT DESC
    ''')
    rows = self.cur.fetchall()
    self.county_extarnal_df = pd.DataFrame(rows)

  def run_main(self):
    """
    Simple demo function that triggers all module functions as a job
    """
    self.write_patients()
    self.run_patients()
    # self.run_patients_external_table()

if __name__ == '__main__':
  dm = DemoModule()
  dm.run_main()
