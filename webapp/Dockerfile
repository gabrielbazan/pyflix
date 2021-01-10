FROM python:3

ENV SOURCES_DIR=webapp

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ${SOURCES_DIR} ${SOURCES_DIR}

CMD python ${SOURCES_DIR}/run.py
