from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdef
from sppy.spapi_cffi_codecs import *
from sppy.spapi_dict import SophiaDict
from sppy.spapi_cursor_dict import SophiaCursorDict
from sppy.spapi_ctl_dict import SophiaCtlDict

#dbname = 'test'
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

ctl_dict =  SophiaCtlDict(sp,ctl)
ctl_dict['sophia.path']='../test_data'
ctl_dict['db']='test'
ctl_dict['db']='test1'
ctl_dict['db']='test2'


rc = sp.open( env )
print "open env",rc._(0)

db1 = ctl_dict['db.test']
db2 = ctl_dict['db.test1']
db3 = ctl_dict['db.test2']

ddb1 =  SophiaDict(dict_db_config,db1)
ddb2 =  SophiaDict(dict_db_config,db2)
ddb3 =  SophiaDict(dict_db_config,db3) 

print "set vals"
for i in xrange(0,keycount):
    ddb1[i]=100+i
    ddb2[i]=1000+i
    ddb3[i]=10000+i

print "get vals"
for i in xrange(0,keycount):
    print ddb1[i]
    print ddb2[i]
    print ddb3[i]

print "cursors"
c1 = SophiaCursorDict(ddb1)
c2 = SophiaCursorDict(ddb2)
c3 = SophiaCursorDict(ddb3)


c1[5]=">="
c2[5]=">="
c3[5]=">="

print [ x for x in c1.iteritems() ]
print [ x for x in c2.iteritems() ]
print [ x for x in c3.iteritems() ]

rc = sp.destroy( env )
print "close env",rc._(0)



