import sys
sys.path.append('../')
#sys.path.append('../cfficodecs')


def open_nv():

    import _spapi_cdef
    from _spapi_cffi import SpApiFFI
    from _spapi_cffi import Wrap

    sp_dl = '../build/sp.so'
    sp = SpApiFFI( sp_dl )

    env = sp.env()
    print "env:",env.cd

    typ = sp.type(env)
    print "typ env?",typ.decode(0)

    ctl = sp.ctl(env)
    typ = sp.type(ctl)
    print "typ ctl?",typ.decode(0)

    rc = sp.set( ctl, "sophia.path", "../test_data/" )
    print "set ctl path", rc.decode(0)

    rc = sp.set( ctl, "db", "spwrap" )
    print "set ctl db name",rc
    db = sp.get( ctl, "db.spwrap" )

    print "db cd",db.cd
    typ = sp.type(db)

    # ._() == .decode()
    print "typ db?",typ._(0)

    rc = sp.open( env )
    print "open env",rc._(0)

    return sp,env,ctl,db



def close_nv (sp, env ):
    rc = sp.destroy( env )
    print "destroy env",rc


def set_int_keys (sp, db, count, int_type):
    itp = int_type+"*"
    for i in xrange(0,count):
        o = sp.object(db)
        key = sp.ffi.new(itp,i)
        szk = sp.ffi.cast("uint32_t",sp.ffi.sizeof(key) )
        rc = sp.set( o, "key",key,szk )
        if rc._(0) == 0: 
            rc = sp.set(db, o)
        else:
            print "err in set key in o"
        if rc._(0) != 0:
            print "err in set key in db"
    #rc = sp.destroy( o )
    print "OK" 
         
def cursor_intkeys( sp, db, it, key, order):
    o = sp.object(db)
    itp = it+"*" 
    ikey = sp.ffi.new(itp,key)
    szk = sp.ffi.cast("uint32_t",sp.ffi.sizeof(ikey) )
 
    sp.set(o,"order",order)
    sp.set(o,"key", ikey, szk )
    cursor = sp.cursor(db, o)
    typ = sp.type(cursor)
    print "cursor?",typ._(0)
    sz = sp.ffi.new("uint32_t*")
   
    o = sp.get( cursor, o ) 
    while o.cd != sp.ffi.NULL:
        key = sp.get(o,"key",sz)
        ckey = sp.ffi.cast(itp,key.cd)
        print ckey[0]
        o = sp.get( cursor, o )



sp, env, ctl, db = open_nv()
set_int_keys( sp, db, 10, "uint16_t")
cursor_intkeys( sp, db,"uint16_t",5,">" )
close_nv(sp, env)
 
