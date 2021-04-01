FROM continuumio/miniconda3 AS build

COPY environment_prd.yaml .
RUN conda env create -f environment_prd.yaml
RUN conda install -c conda-forge conda-pack

COPY . .
RUN conda run -n datascience_prd pip install -e .

RUN conda-pack --ignore-editable-packages \
    -n datascience_prd -o /tmp/env.tar \
    && mkdir /venv \
    && cd /venv \
    && tar xf /tmp/env.tar \
    && rm /tmp/env.tar

RUN /venv/bin/conda-unpack


FROM debian:buster-slim

RUN groupadd -r user \
    && useradd --no-log-init -r -g user user
USER user
ENV PATH=$PATH:/home/user/.local/bin

COPY . /work
WORKDIR /work

SHELL ["/bin/bash", "-c"]

COPY --from=build /venv /venv
ENTRYPOINT source /venv/bin/activate && bash