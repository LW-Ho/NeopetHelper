FROM python:3.8-alpine

USER root

WORKDIR /neopetHelper
COPY . /neopetHelper/

RUN pip install -r requirement.txt

CMD ["python", "dailies.py"]