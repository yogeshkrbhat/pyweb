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
VOLUME /fs
EXPOSE 8080

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080","main:app"]

