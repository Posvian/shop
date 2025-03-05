FROM python:3.11.11

ENV PYTHONUNBUFFERED 1
COPY.env /.env
COPY ./requirements.txt /requirements.txt
#RUN apk add --update --no-cache postgresql-client jpeg-dev
#RUN apk add --update --no-cache --virtual .tmp-build-deps  \
#    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
RUN pip install -r requirements.txt
#RUN apk del .tmp-build-deps

RUN mkdir /src
COPY ./src /src
WORKDIR /src

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
