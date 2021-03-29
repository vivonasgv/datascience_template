




## Running Experiments

- See ([run_experiments.ipynb](run_experiments.ipynb)) to run experiments on featues stored in the Toniq Feature Store
    1. Specify the **Experiment Configuration**
    2. Specify the Models Hyperparameter Configuration you want to run experiments over
- Create your own trainign modules for custom training by inheriting [TrainerManager](../modules/trainer.py)
    

### Experiment Configuration

- Create the following JSON to initialize your experimental state


```json
config = {
"provider": "gcp", # Cloud Provider

"hyperopt": # Hyperparameter (Hyperopt) Arguments
    {
    "metric": "fMeasure", # Chosen Metric to Evaluate
    "max_evals": 100, # Number of Evaluations
    },
    
"mlflow": 
    {
        "experiment_name": "EXP5", # Name of the Experiment
        "tags": {"version": "0.1.0"}  # Addiitonal Tags (Optional)
    },
"data": # Argumens for Extracting Features from Toniq Data Manager
    {
         "train": 
                  {
                       "name": "train_feature_store_path", 
                       "store": "feature", 
                       "partition": "train"
                  },

         "train": 
              {
                   "name": "train_feature_store_path", 
                   "store": "feature", 
                   "partition": "train"
              },

    
    }
}
```
### Model Hyperparemter Space

```python

space = hp.choice('model',      
    [
        {
            'type': 'classification',
            'name': 'RandomForestClassifier',    
            'params': {
                       "maxDepth":hp.quniform("maxDepth",5,10,1),
                       "maxBins":hp.quniform("maxBins", 45,60,1),
                       "minInstancesPerNode":hp.quniform("minInstancesPerNode", 40,60,1),
                       "numTrees":hp.quniform("numTrees", 40,60,1)
                      }
        },
        
        {
            'type': 'classification',
            'name': 'GBTClassifier',   
            
            
            'params': {
                       "maxDepth":hp.quniform("maxDepth_GBT",5,10,1),
                       "maxBins":hp.quniform("maxBins_GBT", 45,60,1),
                       "minInstancesPerNode":hp.quniform("minInstancesPerNode_GBT", 40,60,1),
                      }
        }
    ])


```


## Saved MLFLOW Experiment and Run Overview:

- Each Experiment contians a set of runs 
    - Each Run Contains a a set of saved objects which include
        - **Parameters**: Hyperparameter of the Model
        - **Metrics**: Metrics Logged during the training/evaluation of that model
        - **Artifiacts**:  Additional Objects that may be needed for reviewing/recreating experiments
            - **Saved Model State**: The parameters of the model during the run
            - **Model Predicitons**: Prediction of the models during training/evaluation
            - **Experiment Coniguration**: The configuration used to created hte experiment


### Review Experiments

- You are able to use the MLFLOW client to review your experiments after their completion or even concurrently without issues.

- For a better understanding of retreiving experiments and runs,  walk through [review_experiments.ipynb](review_experiments.ipynb)


### Using Streamlit to Review Experiments

- You can also use Streamlit to review your experiments while or after they run
- Please see the provided [streamlit app for reviewing experiments](streamlit_review_experiments.py)
- To run the app, go to the terminal (in the virtual env you made)

