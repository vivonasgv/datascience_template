

"""Demo Module definition file"""
from module import ToniqEnvManager
import pandas as pd 
import pyspark.sql.functions as f


import warnings
warnings.simplefilter("ignore")


import pandas as pd
import io
import requests
import sys
import json
import plotly.express as px
from data_manager import DataManager


import pyspark.ml
import pyspark.sql.functions as f
import pyspark.sql.types as t

from pyspark.ml.tuning import CrossValidator
from pyspark.mllib.evaluation import MulticlassMetrics

import toniq

'''We Use hyperopt for Optimizations'''
import hyperopt
from hyperopt import hp
from hyperopt import fmin, tpe

from functools import partial

import tempfile
from shutil import make_archive


class ExperimentManager():
  
  '''
  Experiment Manager with MLFLOW
  '''
  def init_mlflow_client(self):
    '''initialize MLFLOW Client'''
    self.mlflow_client = toniq.MlflowClient()

    
  def get_experiment(self):
    '''Initialize MLFLOW Experiment (If it does not exist)'''

    self.experiment= self.mlflow_client.get_experiment_by_name(self.config["mlflow"]["experiment_name"])

    if self.experiment:
      # if the experiment is not None, get the id
      self.experiment_id = self.experiment.experiment_id
    else:
      # if the experiment is None, create a new exerpiment and get the experiment by name
      self.experiment_id= self.mlflow_client.create_experiment(self.config["mlflow"]["experiment_name"])
      self.experiment= self.mlflow_client.get_experiment_by_name(self.config["mlflow"]["experiment_name"])

       
  def create_run(self):
    self.current_run = self.mlflow_client.create_run(self.experiment_id)
    self.run_id = self.current_run.info.run_id
    
    
    


class TrainerManager(DataManager, ExperimentManager):
  """Trainer Manager for Running Experiments"""
  def __init__(self, config):
        
        
    """

    Config Template

    config = {
    "provider": "gcp"
    "hyperopt":
        {
        "metric": "fMeasure",
        "max_evals": 100,
        },

    "mlflow":
        {
            "experiment_name": "EXP3",
            "tags": {"version": "0.1.0"} 
        },
    "data":
        {
             mode: {"name": f"income_transformed_data_{mode}", "store": "feature", "partition": mode}
             for mode in ["train", "test"]

        }
    }
    """

    
    super(TrainerManager, self).__init__(provider=config["provider"])
    # Get DatamManger
    
    self.config = config
    
    
    # Load Dataset
    self.load_data()
    
    # get the experiment if it exists, otherwise it will return a None 
    self.init_mlflow_client()
    
    # init mlflow client
    self.init_mlflow_client()
    self.get_experiment()
    
    

  def load_data(self):
    '''Load Datasets from the Toniq Store'''
    
    self.dfs = {}
    for mode, load_table_args in self.config["data"].items():
      self.dfs[mode]= self.load_table(**load_table_args)
    
  def calculate_metrics(self, df):   
    """

    define your own metrics to evaluate cross validation

    :params:

    df: dataframe containing {aprediction} and {label} columns

    :returns:

    confusion matrix

    """

    # turn gt into label
    preds_and_labels = df.select('prediction',f.col('label').cast(t.FloatType()))
    metrics = MulticlassMetrics(preds_and_labels.rdd.map(tuple))


    # confusion matrix


    metrics_dict = dict(
        # unweighted measures
        tpr = metrics.truePositiveRate(label=1.0),
        fpr = metrics.falsePositiveRate(label=1.0),
        precision = metrics.precision(label=1.0),
        recall = metrics.recall(label=1.0),
        fMeasure = metrics.fMeasure(label=1.0)
    )


    metrics_dict= {k:round(v,3) if  k != "confusion" else v for k,v in metrics_dict.items()}


    return metrics_dict

    
  def run_experiment(self, model_config):
    '''
    Run the Experiment
    '''
    
    '''update the model config'''
    self.config["model"] = model_config
    
    '''get the model'''
    model = getattr(getattr(pyspark.ml, model_config["type"]), model_config["name"])
    model = model(**model_config["params"])
    
    
    """CREATE A NEW RUN"""
    self.create_run()
    
    
    '''
    
    Training and Evaluating Model
    
    '''
    
    
    '''Fit the Model on the Training Set'''
    model = model.fit(self.dfs["train"])
    
    '''Infer Model On Training and Testing Set'''
    pred_dfs = {mode:model.transform(df) for mode, df in self.dfs.items()}
    
    
    
    '''Calculate Metrics on Training and Testing Set'''
    metric_results= {mode: self.calculate_metrics(pred_df) for mode,pred_df in pred_dfs.items()}
    self.config["metrics"] = metric_results
    
            
        
    '''
    
    MLFLOW Logging 
      Metrics
      Parameters
      Artifacts
        - Model State
        - Predictions from Model
        - config
    
    '''
    
        
        
        
        
    '''Register Metrics in MLFLOW'''
    for mode in metric_results.keys():
        for metric_key, metric_val in metric_results[mode].items():
            self.mlflow_client.log_metric(self.run_id, f"{mode}-{metric_key}", metric_val)
    
    
    
    
    
    
    '''Register Model Parameters in MLFLOW'''
    for param_name, param_val in self.config["model"]["params"].items():
        self.mlflow_client.log_param(self.run_id,param_name, param_val)
    
    
    
    
    
    
    '''Save Predictions as Artifact (Pandas Dictionary)'''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as fp:
        # SAVE TEST PREDICTIONS ONLY FOR DEMO TO SAVE SPACE
        pred_dfs["test"].createOrReplaceTempView("pred_df")
        
        #To save as a pandas array to json , we need to use a udf to conver the vector into an array
        self.spark.udf.register("TOARRAY", lambda v: v.toArray().tolist(), t.ArrayType(t.FloatType()))
        tmp_df = self.spark.sql("""
            SELECT 
                label,
                TOARRAY(probability) as probability,
                prediction

            FROM pred_df
        """).toPandas()
        # save dataframe to json
        tmp_df.to_json(fp.name)
        
        # log the predictions as an artifact
        self.mlflow_client.log_artifact(self.run_id ,fp.name, artifact_path="predictions")
       
    
    
    
    
    
    '''Save Model as an Artifact'''
    with tempfile.TemporaryDirectory() as dp:
        # Note the mode is 'w' so json could be dumped
        # Note the suffix is .txt so the UI will show the file
        """write model to temprorary directory"""
        model.write().overwrite().save(dp)
        self.mlflow_client.log_artifact(self.run_id ,dp, artifact_path="model")
        
        
        
        
        
        
        
        
    
    '''Save Config of Experiment and Run '''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as fp:
        # Note the mode is 'w' so json could be dumped
        # Note the suffix is .txt so the UI will show the file
        json.dump(self.config, fp)
        fp.seek(0)
        self.mlflow_client.log_artifact(self.run_id ,fp.name, artifact_path="config")
            
    '''RETURN metric to Optimizer * (-) for minmizing negative (aka, maximize positive score)'''
    
    chosen_hyperopt_score = -metric_results["test"][self.config["hyperopt"]["metric"]]
    
    
    '''terminate run, otherwise Run Status will be active Hereafter'''
    self.mlflow_client.set_terminated(self.run_id)
    
    return chosen_hyperopt_score