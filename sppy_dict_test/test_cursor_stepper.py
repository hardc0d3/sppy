from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdef
from sppy.spapi_cffi_codecs import *
from sppy.spapi_dict import SophiaDict
from sppy.spapi_cursor_dict import CurrentStep, SophiaCursorDict
dbname = 'test'
sp = SophiaApi( '../../sophia/libsophia.so.1.2.1',sophia_api_cdef )
codec_u32 = U32(sp.ffi)
dict_db_config = {
'sp.api':sp
,'key.codec':codec_u32
,'value.codec':codec_u32
}

keycount = 10

env = sp.env()
print "get env object",env.cd

typ = sp.type(env)
print "type env env?",typ.decode(0)

ctl = sp.ctl(env)
typ = sp.type(ctl)
print "type of ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", "../test_data/" )
print "set ctl path", rc.decode(0)


rc = sp.set( ctl, "db", dbname )
print "set ctl db name:%s"%dbname,rc

rc = sp.open( env )
print "open env",rc._(0)

db = sp.get( ctl, "db.%s"%dbname )
print "get ctl db.%s"%dbname,db.cd

typ = sp.type(db)
print "db type",typ._(0)

dict_db =  SophiaDict(dict_db_config,db)


print "set vals"
for i in xrange(0,keycount):
    dict_db[i]=1000+i

print "get vals"
for i in xrange(0,keycount):
    print dict_db[i]



SC = SophiaCursorDict

c1,c2,c3,c4 = SC(dict_db), SC(dict_db), SC(dict_db), SC(dict_db)
c1[3]="<"
c2[3]="<="
c3[3]=">"
c4[3]=">=" 

print "test iterator"

stepper = CurrentStep(iter(c1))
print stepper.cnt,stepper.current()
while True:
   try:
       stepper.step()
       print stepper.cnt, stepper.current()
   except StopIteration, e:
       break
       
 




