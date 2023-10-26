# syntax=docker/dockerfile:1
# Pull official base image
FROM python:3.10-slim

# Set working directory
WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional \
    build-essential libpq-dev binutils libproj-dev gdal-bin

COPY poetry.lock pyproject.toml /code

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
# Install dependencies
RUN poetry install

COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]

CMD ["/code/run.sh"]
