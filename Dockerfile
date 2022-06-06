FROM python:3.10.4
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./pg ./pg

CMD ["python3", "./pg/manage.py", "runserver", "0.0.0.0:8000"]