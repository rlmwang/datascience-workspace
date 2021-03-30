FROM continuumio/miniconda3 AS build

COPY environment_dev.yaml .
RUN conda env create -f environment_dev.yaml
RUN conda install -c conda-forge conda-pack

RUN conda-pack -n datascience_dev -o /tmp/env.tar \
    && mkdir /venv \
    && cd /venv \
    && tar xf /tmp/env.tar \
    && rm /tmp/env.tar

RUN /venv/bin/conda-unpack


FROM debian:buster-slim
COPY --from=build /venv /venv

RUN groupadd -r user \
    && useradd --no-log-init -r -g user user
USER user
ENV PATH=$PATH:/home/user/.local/bin

WORKDIR /work

SHELL ["/bin/bash", "-c"]
ENTRYPOINT source /venv/bin/activate && bash