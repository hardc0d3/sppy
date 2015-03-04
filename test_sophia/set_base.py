import sys
import time
sys.path.append('../')
sys.path.append('../cfficodecs')
import _spapi_cdef
from cfficodec import BaseCtoPy
from _spapi_cffi import SpApiFFI
from _spapi_cffi import Wrap
from sppy import Env
from sppy import DB


sp_dl = '../build/sp.so'

spapi = SpApiFFI( sp_dl )


env  = Env( spapi, "/dataset/env1")
#print "env open",env.open()

db = DB( env, "sophia_base_test")
codec = BaseCtoPy(env.sp)

#print "db open",db.open()
print "env open",env.open()

count = 100000

print "set from 1 to %d string keys" % (count-1)
s = time.time()
for i in xrange(1,count):
    key = "%d" % (i)
    val = "test string val %d" % i
    db.set_s_s( key,val )
e = time.time()
es = e - s
print "t",es
print ""

print "close env",env.close()






