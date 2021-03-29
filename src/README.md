

## ML Experiment Pipeling Overview


1. **Extract**: Scripts for Extacting Raw Data
    - [**extract.ipynb**](extract_data/extract.ipynb): Extract Raw Features and Save into Datastore
2. **Transform**: Scripts for Transforming Raw Data into Features
    - [**streamlit_transform.py**](transform_data/streamlit_transform.py): Review Raw Features before tranforming them.
    - [**transform.ipynb**](transform_data/transform.ipynb) : Transform features and save in Feature Datastore
3. **Experiment**: Scripts for Running Experiments on Transformed Data
    - [**Run Experiments**](experiments/run_experiments.ipynb): Run Experiments and Save results (metrics, parameters, artifacts) into MLFLOW.
    - [**Review Experiments**](experiments/review_experiments.ipynb): Review Previously Runned Experiments In a Notebook. 
        - [**streamlit_review_experiments.py**](experiments/streamlit_review_experiments.py): You can also use streamlit to review runs and experiments logged in MLFLOW 
