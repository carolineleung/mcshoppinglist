#!/bin/bash

MONGO_HOME=/opt/mongodb/mongodb-current
#export PATH=${MONGO_HOME}/bin:${PATH}
MONGO_DATA=/srv/mongodb/mcshoppinglist/development
NOHUP_LOG=/tmp/mongodb_nohup.out
nohup ${MONGO_HOME}/bin/mongod --dbpath ${MONGO_DATA}/db --journal --logpath ${MONGO_DATA}/logs/mongodb.log --logappend > ${NOHUP_LOG} 2>&1 &
sleep 1
cat ${NOHUP_LOG} 

