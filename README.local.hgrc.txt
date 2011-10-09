# For your clone, to skip typing u/p each time:
# gvim yourrepo\.hg\hgrc
##### 
[auth]
foo.prefix = hg.intevation.org/mercurial
foo.username = foo
foo.password = bar
foo.schemes = http https
######




# on windows, to use the unverified ssl certificate
# avoid: abort: error: _ssl.c:480: error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed
# https://bitbucket.org/tortoisehg/thg/issue/63/cannot-pull-push-to-https-server-with-self	
# gvim %USERPROFILE%\mercurial.ini
# add:

[web]
cacerts=






# gvim %USERPROFILE%\mercurial.ini
# add (without underscores ___):
________________________

[web]
cacerts=

________________________



# Clone:

cmd
hg clone https://m1.xen.prgmr.com/hg/mcshoppinglist

username: yourusername
password: will send in IM



# gvim .\mcshoppinglist\.hg\hgrc
# Add:
_________________________

[auth]
m1.prefix = https://m1.xen.prgmr.com/hg
m1.username = yourusername
m1.password = yourpassword

_________________________



