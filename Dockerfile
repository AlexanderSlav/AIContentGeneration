FROM python:3.10

WORKDIR /workdir

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONPATH $PYTHONPATH:/workdir/src

COPY ./ ./
