#!/bin/sh

datetime=`date +"%Y%m%d%H%M%S"`
appname='cd-heatmap-portal'

# docker build
docker build -t ${appname}:${datetime} .

# force change tag :latest
docker tag ${appname}:${datetime} ${appname}

# restart
docker stop ${appname}
docker rm ${appname}

# docker run
docker run -d -p 28020:80 -v /etc/localtime:/etc/localtime --restart=always --name=${appname} ${appname}

# clean
docker images |awk '{print $3}' |xargs docker rmi
