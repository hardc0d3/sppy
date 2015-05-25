from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdef 
from sppy.spapi_cffi_codecs import *

sp = SophiaApi( '../../sophia/libsophia.so.1.2.1',sophia_api_cdef )

codec_u32 = U32(sp.ffi)

env = sp.env()
print "get env object",env.cd

typ = sp.type(env)
print "type env env?",typ.decode(0)

ctl = sp.ctl(env)
typ = sp.type(ctl)
print "type of ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", "../test_data/" )
print "set ctl path", rc.decode(0)

rc = sp.open( env )
print "open env",rc._(0)

rc = sp.destroy(env)
print "destroy env",rc



