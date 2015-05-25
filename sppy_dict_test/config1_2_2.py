from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdefs 
from sppy.spapi_cffi_codecs import *
#from sppy.spapi_dict import SophiaDict
#:from sppy.spapi_cursor_dict import SophiaCursorDict
default_sp_path = '../test_data'
default_db_name = 'test'
sp = SophiaApi( '../../sophia/sophia1.2.2/libsophia.so.1.2.2',sophia_api_cdefs['1.2.2'] )
codec_u32 = U32(sp.ffi)
dict_db_default_config = {
'sp.api':sp
,'key.codec':codec_u32
,'value.codec':codec_u32
}
keycount = 10

