# syntax=docker/dockerfile:1
FROM python:3.10

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin

ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY requirements/*.txt /code/requirements/
RUN pip3 install -r requirements/requirements.txt --src /usr/local/src

COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]

CMD ["/code/run.sh"]