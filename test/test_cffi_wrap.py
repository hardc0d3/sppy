import sys
sys.path.append('../')
sys.path.append('../cfficodecs')

import _spapi_cdef
from _spapi_cffi import SpApiFFI
from _spapi_cffi import Wrap

sp_dl = '../build/sp.so'

sp = SpApiFFI( _spapi_cdef.cdef, sp_dl )

env = sp.env()
print "env:",env.cd
typ = sp.type(env)
print "typ",typ.decode()
ctl = sp.ctl(env)
typ = sp.type(ctl)
print "typ",typ.decode()
rc = sp.set( ctl, "sophia.path", "../test_data/" ) 
print "set ctl path", rc.decode()
rc = sp.set( ctl, "db", "spwrap" )
print "set ctl db name",rc
rc = sp.open( env )
print "open env",rc._()
rc = sp.destroy( env)
print "close env",rc._()

