FROM python:3.10-alpine

COPY . /proxy
WORKDIR /proxy

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "proxy.py"]
