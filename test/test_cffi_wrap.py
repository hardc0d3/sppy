
import sys
sys.path.append('../')
sys.path.append('../cfficodecs')

import _spapi_cdef
from _spapi_cffi import SpApiFFI
from _spapi_cffi import Wrap

sp_dl = '../build/sp.so'

sp = SpApiFFI( _spapi_cdef.cdef, sp_dl )


env = sp.env()
sptype = sp.type(env)
print sptype.decode()
ctl = sp.ctl(env)
sptype = sp.type(ctl)
"decode shortland is _"
print sptype._()

