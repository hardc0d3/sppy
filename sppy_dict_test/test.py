from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_codecs import *
from sppy.spapi_dict import SophiaDict
import config1_2_2 as conf

dbname = conf.default_db_name
sp = conf.sp
codec_u32 = conf.codec_u32 
dict_db_config = conf.dict_db_default_config 
keycount = conf.keycount 

env = sp.env()
print "get env object",env.cd

typ = sp.type(env)
print "type env env?",typ.decode(0)

ctl = sp.ctl(env)
typ = sp.type(ctl)
print "type of ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", conf.default_sp_path )
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

print "change vals"
for i in xrange(0,keycount):
    dict_db[i]=i+100

print "get vals"
for i in xrange(0,keycount):
    print dict_db[i]

print "del keys"
for i in xrange(0,keycount):
    del dict_db[i]

print "set key only"
for i in xrange(0,keycount):
    dict_db[i]=None

print "get vals"
for i in xrange(0,keycount):
    print dict_db[i]


rc = sp.destroy(db)
print "destroy db",rc._(0)

rc = sp.destroy(env)
print "destroy env",rc._(0)



