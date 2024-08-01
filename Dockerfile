#**************************************
# Build By:
# https://itheo.tech 2021
# MIT License
# Dockerfile to run the python script
#**************************************

FROM python:3.11.0-slim-buster as base

LABEL org.opencontainers.image.authors="info@itheo.tech"
ENV TZ=Europe/Amsterdam

RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get install -y locales && \
    apt-get -y autoremove

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# en_GB.UTF-8 UTF-8/en_GB.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# nl_NL.UTF-8 UTF-8/nl_NL.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

RUN pip install poetry

WORKDIR /src

COPY poetry.lock .
COPY pyproject.toml .
COPY ./src .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM base as dev
ENV PY_ENV=dev
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

FROM base as acc
ENV PY_ENV=acc
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

FROM base as PROD
ENV PY_ENV=prod
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
