#!/bin/sh

datetime=`date +"%Y%m%d%H%M%S"`
appname='cd-heatmap-server'

# docker build
docker build -t ${appname}:${datetime} .

# force change tag :latest
docker tag ${appname}:${datetime} ${appname}


docker stop ${appname}
docker rm ${appname}

# docker run
docker run -d -p 28021:5050 -v /etc/localtime:/etc/localtime -v /var/log/${appname}:/src/log --restart=always --name=${appname} ${appname}

# clean
docker images |awk '{print $3}' |xargs docker rmi
