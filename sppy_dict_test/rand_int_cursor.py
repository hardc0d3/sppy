from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_codecs import *
from sppy.spapi_dict import SophiaDict
from sppy.spapi_cursor_dict import SophiaCursorDict
import config1_2_2 as conf
from random import randint

dbname = conf.default_db_name
sp = conf.sp
codec_u32 = conf.codec_u32
dict_db_config = conf.dict_db_default_config



env = sp.env()
ctl = sp.ctl(env)

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

keycount = 40
l=[0]*keycount

for i in xrange(0,keycount):
    l[i]=randint(1000,2000)

import list_data
l = list_data.l
l=list(set(l))
keycount = len(l)
#print l


print "set vals"
for i in xrange(0,keycount):
    try:
        kk = dict_db[l[i]] 
        #print kk
    except KeyError:
        dict_db[l[i]]=l[i]


#print "get vals"
#for i in xrange(0,keycount):
#    print dict_db[l[i]],



SC = SophiaCursorDict

c = SophiaCursorDict(dict_db)

c[1500]=">="

print list(c)
