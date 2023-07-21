FROM python:latest

COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

ADD server.py /

# RUN python3 main.py