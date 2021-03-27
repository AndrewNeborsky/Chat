# Chat #

A small functional person-to-person message center application built using Django.

------------

#### To work the project you need [Redis](https://redis.io/) and the following modules:

- [Django](https://github.com/django/django)
- [Django Channels](https://github.com/django/channels)
- [channels_redis](https://github.com/django/channels_redis/)
- [Pillow](https://github.com/python-pillow/Pillow)
- [Redis-py](https://github.com/andymccurdy/redis-py)

------------

#### Run project in docker:

```bash
$ docker build -t chat:v1 .
$ docker run -d -p 80:8000 chat:v1
```

Chat will start on http://127.0.0.1/

------------
