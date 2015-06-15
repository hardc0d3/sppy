from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_codecs import *
from sppy.spapi_dict import SophiaDict
from sppy.spapi_cursor_dict import SophiaCursorDict
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


rc = sp.set( ctl, "db.%s.index.cmp", "u32" )


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

print "test iter"

print c1.key,c1.order, [ x for x in c1 ]
print c2.key,c2.order, [ x for x in c2 ]
print c3.key,c3.order, [ x for x in c3 ]
print c4.key,c4.order, [ x for x in c4 ]

print "reset cursors"

c1.reset()
c2.reset()
c3.reset()
c4.reset()

print "test iteritems"

print c1.key,c1.order, [ x for x in c1.iteritems() ]
print c2.key,c2.order, [ x for x in c2.iteritems() ]
print c3.key,c3.order, [ x for x in c3.iteritems() ]
print c4.key,c4.order, [ x for x in c4.iteritems() ]



