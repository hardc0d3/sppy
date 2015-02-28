import sys
sys.path.append('../')
sys.path.append('../cfficodecs')

import _spapi_cdef
from _spapi_cffi import SpApiFFI

global sp_sodll, SP_PATH, sp_path, SP_DB, sp_db, sp_db_key
SP_PATH = 'sophia.path'
sp_path = '../test_data/spapi_env'
SP_DB = 'db'
sp_db = 'spapi_cffi_test'
db_key = SP_DB + "." +  sp_db
sp_dl = '../build/sp.so'

sp = SpApiFFI( _spapi_cdef.cdef, sp_dl )
def e_s ( s ):
    return sp.ffi.new("char []",s)
def e_s_sz( s, sz ):
    return sp.ffi.new("char [%d]",s)
def e_u32( u32 ):
    return sp.ffi.cast("uint32_t",u32)
 
def u_ ( i ):
    return sp.ffi.cast("uint32_t",i)

def sz_ ( cd ):
    return sp.ffi.cast("uint32_t",sp.ffi.sizeof( cd ) )


def str_ ( vp ):
    #global sp
    return sp.f.string( sp.f.cast("char *", vp) )

def cs_test():
    print "e_ ncode d_ ecode string == ", e_s( "string") 
    
null = sp.ffi.NULL


def sp_init():
    global db,env,ctl
    env = sp.env()
    #print env
    #exit()
    #print  sp.type(env.o) 
    ctl = sp.ctl( env.o )
    #print ( sp.type(ctl) )
    r = sp.set( ctl.o, e_s(SP_PATH), e_s(sp_path) )
    print r 
    r = sp.set( ctl.o, e_s(SP_DB), e_s(sp_db) )
    print r
    db = sp.get( ctl.o, e_s(db_key) )
    #print d_( sp.type(db) ) , db
    r = sp.open(env.o)
    print "open env",r 
   

def sp_set_data():
    global db,obj
    obj = sp.object(db)
    if obj != null:
        #print d_( sp.type(obj) )
        key = e_s("thekey")
        val = e_s("theval")
        #print key,val,szk,szv
        rk = sp.set( obj, e_s("key"), key, sz_(key)  )
        rv = sp.set( obj, e_s("value"),val, sz_(val)  )
        print "sp set obj k,v",rk,rv
        rc = sp.set(db,obj)
        print "sp set obj in db", rc
    if obj != null:
        r = sp.destroy( obj )
        print "obj destroy", r

def sp_get_data():
    global db,obj
    if db==null:
        return None
    obj = sp.object(db)
    key = e_s("thekey")  
    r = sp.set( obj, e_s("key"),key, sz_(key) )
    print "query set key", r
    res = sp.get(db, obj )
    print res
    if res == null:
        return None
    sz = sp.ffi.new("uint32_t*")
    val = sp.get(obj,e_s("value"),sz )
    print sz[0],val,sp.ffi.buffer(val,sz[0])[:]


def sp_destroy():
    global db, env 
    if db != null:
        r = sp.destroy( db )
        print "db destory" ,r
    if env != null:
        r = sp.destroy( env.o )
        print "env destroy", r





cs_test()
sp_init()
sp_set_data()
sp_get_data()
sp_destroy()



