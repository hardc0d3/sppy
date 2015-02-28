import sys
sys.path.append('../')
sys.path.append('../cfficodecs')

import _spapi_cdef
from _spapi_cffi import SpApiFFI
from cfficodec import CharString

global sp_sodll, SP_PATH, sp_path, SP_DB, sp_db, sp_db_key
SP_PATH = 'sophia.path'
sp_path = '../test_data/spapi_env'
SP_DB = 'db'
sp_db = 'spapi_cffi_test'
db_key = SP_DB + "." +  sp_db
sp_dl = '../build/sp.so'

global sp,cs
sp = SpApiFFI( _spapi_cdef.cdef, sp_dl )
cs = CharString( sp.ffi, sp.lib )
enc = cs.encode
dec = cs.decode

def sp_str ( vp ):
    #global sp
    return sp.f.string( sp.f.cast("char *", vp) )

def cs_test():
    print "encode decode string == %s" % dec(enc( "string") )
    
global null
null = sp.ffi.NULL


def sp_init():
    env = sp.env()
    print sp_str( sp.type(env) )
    ctl = sp.ctl( env )
    print sp_str( sp.type(ctl) )
    r = sp.set( ctl, enc(SP_PATH), enc(sp_path) )
    print r 
    r = sp.set( ctl, enc(SP_DB), enc(sp_db) )
    print r
    db = sp.get( ctl, enc(db_key) )
    print sp_str( sp.type(db) ) , db

cs_test()
sp_init()

