#!/bin/bash

MONGO_HOME=/opt/mongodb/mongodb-current
${MONGO_HOME}/bin/mongo --eval "db._adminCommand(\"shutdown\");"

