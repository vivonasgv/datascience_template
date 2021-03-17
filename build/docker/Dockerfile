ARG CRESTLE_NAME=us.gcr.io/terraform-254700/amplified/toniq-notebook-ckexdk2nk00002f940emg3gqi
ARG CRESTLE_VERSION=0.9.0

FROM $CRESTLE_NAME:$CRESTLE_VERSION AS build-core

###
# Simple base Crestle image customization to add module code
###

# TODO: include mc client on base notebook image
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x mc && mv mc /usr/local/bin/

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install module locally on the image
RUN pip install -e .

# Override with local reference of Toniq SDK until we have pypi
RUN pip install -e ./toniq-sdk-python

# Entrypoint should be customized with Helm templates YAML
# CMD [ "python", "-m", "scripts.demo.test-toniq.py"]