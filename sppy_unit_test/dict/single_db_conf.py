from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdefs
from sppy.spapi_cffi_codecs import *

sophia_dl = '../../lib/sophia/libsophia.so.1.2.2'
scene_dir = '../../test_data/single_db'
db_name   = 'test_db'
sp = SophiaApi( sophia_dl, sophia_api_cdefs['1.2.2'] )
max_val = 4294967295
items = 100
start = max_val - items
stop = max_val
offset = 1000

u32 = U32(sp.ffi)
dict_db_conf = {
'sp.api':sp
,'key.codec':u32
,'value.codec':u32
}


