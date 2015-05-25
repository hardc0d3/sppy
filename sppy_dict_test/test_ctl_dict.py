from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_codecs import *
from sppy.spapi_dict import SophiaDict
from sppy.spapi_cursor_dict import SophiaCursorDict
from sppy.spapi_ctl_dict import SophiaCtlDict

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

ctl_dict =  SophiaCtlDict(sp,ctl)
ctl_dict['sophia.path'] = conf.default_sp_path
ctl_dict['db']=dbname


rc = sp.open( env )
print "open env",rc._(0)

db = ctl_dict['db.%s'%dbname]

typ = sp.type(db)
print "db type",typ._(0)


print  "--- test ctl cursor iter kitems ( keymval) ---"

for ctl_k, ctl_v in ctl_dict.iteritems():
    print ctl_k,ctl_v

print "--- test iter keys----"

for ctl_key in ctl_dict:
    print ctl_key,ctl_dict[ctl_key] 


rc = sp.destroy( env )
print "close env",rc._(0)



