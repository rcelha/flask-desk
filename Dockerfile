FROM python:3-onbuild

ADD requirements.txt /requirements.txt
ADD flask_desk /code/flask_desk

WORKDIR /code/flask_desk

EXPOSE 5000

RUN useradd ispm0
RUN useradd ispm1
RUN useradd ispm2

CMD ["python", "app.py"]
