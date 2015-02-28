import sys
sys.path.append('../')
sys.path.append('../cfficodecs')

import _spapi_cdef
from _spapi_cffi import SpApiFFI
from cfficodec import CharString


SP_PATH = "sophia.path"
sp_path = "../test_data/sp_test_env1"
SP_DB = "db"
db_name = "env1test"
db_key = SP_DB+"."+db_name

def sp_type( sp,vp ):
    return sp.f.string(sp.f.cast("char *",sp.sptype( res = vp )) )


sp = SpApiFFI( _spapi_cdef.cdef, '../build/sp.so' )
cs = CharString( sp.ffi, sp.lib )

_ = cs.encode
__ = cs.decode
null = sp.ffi.NULL

print ""
print "test char string codec string == %s" %__( _( "string") )

def init_env_ctl_db():
    print "init_env_ctl_db"
    global env,ctl,db

    env = sp.env()
    print env
    print sp_type(sp,env)

    ctl = sp.ctl(env = env )
    print ctl
    print sp_type(sp,ctl)

    r = sp.set( ctl, _( SP_PATH ), _( sp_path ) )
    print "set env path", r
    r = sp.set( ctl, _( SP_DB ), _( db_name ) )
    print "set db name", r
    db = sp.get( ctl, _( db_key ) )

    print db
    print sp_type(sp,db)


def open_env_destroy_env():
    print "open_env_destroy_env"
    global env
    print "open env"
    r = sp.open( env = env )
    print r
    print "destroy env"
    r = sp.destroy( res = env )
    print r

def open_env_destroy_db_destroy_env():
    print "open_db_destroy_db_destroy_env"
    global env,db
    print "open db"
    r = sp.open(env = env )
    print r
    print "destroy db"
    r = sp.destroy( res = db )
    print  r
    print  "destroy env"
    r = sp.destroy( res = env )
    print r


# create test cases
def open_db_destroy_db_destroy_env():
    print "open_db_destroy_db_destroy_env"
    print "open db" 
    r = sp.open(db = db )
    print r
    print "destroy db"
    r = sp.destroy( res = db )
    print  r
    print  "destroy env"
    r = sp.destroy( res = env )
    print r





init_env_ctl_db()
open_env_destroy_env()
init_env_ctl_db()
open_db_destroy_db_destroy_env()
init_env_ctl_db()
open_env_destroy_db_destroy_env()

