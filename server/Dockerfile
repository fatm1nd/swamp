FROM python:latest

COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

ADD server.py /
ADD .env /
ADD database.py /
ADD hashGenerator.py /
ADD shrek_script.txt /

# RUN python3 main.py