FROM python:3.8-slim-buster as test
WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
COPY . .
RUN python3 -m unittest -v

FROM python:3.8-slim-buster
WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "main.py" ]