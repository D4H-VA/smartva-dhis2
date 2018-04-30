FROM python:3.6-stretch

RUN apt-get update && apt-get install -y --no-install-recommends openjdk-8-jre

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
CMD ["python", "-m", "smartvadhis2"]