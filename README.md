# Toniq Demo Module

This module was generated from the CookieCutter template at: https://github.com/doc-ai/toniq-ds-cookiecutter

## Repository Folder Structure

- **docs**: Any documents relating to your project
- **references**: Any reference material you include in your project

- **reports**: Reports from your projects, ex. PDFs etc
    - **figures**: Store Figures

- **data**:
    - **raw**: raw data files
    - **interim/processed**: itermediate data processed from raw
    - **external**: external datasets

- **models**: Stored Models during Experiments

- **src**: Source Files Containing your Experiment DAG
    - **data**: Scripts for loading Raw Data
    - **features**: Scripts for Preprocessing Raw Data
    - **models**: Scripts for training and testing the model
    - **visualization**: Scripts for visualizating experimental outputs along hte pipeline
    - **demo_module**: Demo module code to be overridden by users

## Quickstart

After generating this repo with `cookiecutter`, run the following commands to get started:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Run linter and tests

For testing we need to install the Toniq SDK as a submodule first so it can be required by the unit tests:

```
pip install -r requirements.test.txt
```

Then run `lint` and `test`:

```
make lint
make test
```

## Deployments

This module can be deployed with Helm in two ways:

1) Directly through the `./deployments/deploy.sh` script
2) Via Cloud Build

### Choosing a deployment target

Also, this module exposes three deployment tasks:

- Main module job: used for data import and preprocessing
- Module app: used for deploying a Streamlit app to visualize data produced by the module
- Install notebooks: install the chosen notebookso on the target Toniq environment

Each task can be enabled for deployment to a given target on the values files found at `deployments/helm_vars/`. We
only need to toggle each task as needed:

```
job:
  enabled: true
  ...
...

app:
  enabled: true
  ...
...

notebooks:
  enabled: true
  ...
...
```

### Manual deployments

The module can be deployed locally as long as we have enough permissions to connect to the remote Kubernetes cluster. `deploy.sh`
expects three arguments:

- cluster: Kubernetes cluster to deploy to
- target: target task, can be `app`, `data` or `all`
- env: `internal`, `staging` or `prod`

```
./deployments/deploy.sh <cluster> <target> <env>
```

The combination of `target` and `env` allows `deploy.sh` to find the values file for deployment. For example, `data` for target
and `staging` for env will feed Helm the values file at `deployments/helm_vars/staging-data/values.yaml`.

### Cloud Build deployments

There are two Cloud Build files in this repo:

- `cloudbuild_build.yaml` for building the Docker image
- `cloudbuild_deploy.yaml` for deploying the module

Cloud Build triggers need to be setup by a user with enough permissions on the target GCP projects and Kubernetes cluster.
