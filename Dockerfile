FROM python:3-onbuild

ADD requirements.txt /requirements.txt
ADD flask_desk /code/flask_desk

WORKDIR /code/flask_desk

EXPOSE 5000

CMD ["python", "main.py"]
