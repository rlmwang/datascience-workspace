FROM continuumio/miniconda3 AS build

COPY requirements_prd.yaml .
RUN conda env create -f requirements_prd.yaml
RUN conda install -c conda-forge conda-pack

RUN conda-pack \
    -n datascience_prd \
    -o /tmp/env.tar \
    && mkdir /venv \
    && cd /venv \
    && tar xf /tmp/env.tar \
    && rm /tmp/env.tar

RUN /venv/bin/conda-unpack


FROM debian:buster-slim
ARG UID
ARG GID

RUN groupadd -r -g $GID docker \
    && useradd -r -u $UID -g docker user

RUN mkdir -p /work \
    && chown -R user /work

RUN mkdir -p /resources \
    && chown -R user /resources

ENV PATH=$PATH:/home/user/.local/bin
USER user

COPY . /work
WORKDIR /work

SHELL ["/bin/bash", "-c"]

COPY --from=build /venv /venv
ENTRYPOINT source /venv/bin/activate && bash