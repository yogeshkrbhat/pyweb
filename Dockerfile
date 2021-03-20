FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt


FROM base

COPY --from=builder /install /usr/local
COPY app /app
WORKDIR /app

CMD ["gunicorn", "-w 4", "0.0.0.0:8080","main:app"]

