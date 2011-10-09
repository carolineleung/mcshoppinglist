#!/bin/bash
#
# http://www.selenic.com/mercurial/hgrc.5.html#web
# 
echo Launching hg server on 8000
hg serve --config web.allow_push=* --config web.push_ssl=False --accesslog ../hgserve.access.log --errorlog ../hgserve.error.log

