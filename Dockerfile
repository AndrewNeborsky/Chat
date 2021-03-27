FROM alpine

WORKDIR /Chat/

VOLUME /Chat/

COPY ./ /Chat/

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo jpeg-dev zlib-dev \
    && apk add redis py3-pip \
    && pip install Django channels channels-redis redis Pillow

EXPOSE 8000

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
