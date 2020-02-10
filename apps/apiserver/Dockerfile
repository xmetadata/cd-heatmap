# python:buster is 3.{latest}
FROM python:buster

LABEL maintainer="xmetadata.com"

COPY ./sources.list /etc/apt/sources.list

RUN ["apt-get", "update"]

RUN ["apt-get", "-y", "install", "libgeos-dev"]

COPY . /src

RUN pip install -r /src/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 5050

ENTRYPOINT ["python", "/src/app.py"]
