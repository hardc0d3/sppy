import sys
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




env  = Env( spapi, "../test_data/env1")
#print "env open",env.open()

db = DB( env, "sophia_base_test")
codec = BaseCtoPy(env.sp)

#print "db open",db.open()
print "env open",env.open()

u32 = codec.cast_uint32_t


db.set_s_s("test1","test_1")
db.set_s_s("test2","test_2")

db.set_u_s(1000,"test_1000")
db.set_u_s(10000,"test_10000")

print db.get_s("test1")
print db.get_s("test2")
print db.get_u(1000)
print db.get_u(10000)




print "close db", db.close()
print "close env",env.close()






