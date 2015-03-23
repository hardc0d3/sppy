import sys
import config
sys.path.append('../')
sys.path.append('../compare_fun')


def set_nv():

    import _spapi_cdef
    from _spapi_cffi import SpApiFFI
    from _spapi_cffi import Wrap

    sp = SpApiFFI( config.spdl )

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
    
    return sp, env, ctl

def open_nvdb(sp, env, ctl):

    db = sp.get( ctl, "db.spwrap" )


    print "db cd",db.cd
    typ = sp.type(db)

    # ._() == .decode()
    print "typ db?",typ._(0)

    rc = sp.open( env )
    print "open env",rc._(0)

    return db


def set_custom_comparsion(sp, ctl):
    import cffi
    import cmpdef
    ffi = cffi.FFI()
    ffi.cdef( cmpdef.cdef )
    lib = ffi.dlopen(config.cmpdl)
    compare_fun  = ffi.new("char[64]")
    compare_fun_arg = ffi.new("char[64]")

    rcc = lib.print_pointer( compare_fun, ffi.cast("size_t",64) , lib.compare_str )
    print "print pointer",rcc
    offset = 0
    rcc = lib.print_pointer( compare_fun_arg, ffi.cast("size_t",64) , ffi.new("size_t*",offset) )
    # sp_set(ctl, "db.name.index.cmp", pointer_fun, pointer_arg);
  # set custom comparsion
    rc = sp.set(ctl, "db.spwrap.index.cmp", compare_fun, compare_fun_arg )
    print "set custom cmp",rc._(0)




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

def set_str_key(sp, db, strkey ):
    o = sp.object(db)
    szk = sp.ffi.cast("uint32_t", len(strkey) )
    rc = sp.set(o, "key", strkey, szk )
    # check
    if rc._(0) != 0: print "err set key object"
    rcd = sp.set(db, o)
    if rcd._(0) != 0: print "err set key in db"

def get_str_key(sp, db, strkey ):
    o = sp.object(db)
    szk = sp.ffi.cast("uint32_t", len(strkey) )
    rc = sp.set(o, "key", strkey, szk )
    # check
    if rc._(0) != 0: print "in get err set key object"
    ret_o = sp.get(db, o)
    if ret_o.cd == sp.ffi.NULL: print "err get key from db"
    sz = sp.ffi.new("uint32_t*")
    ret_key = sp.get(ret_o,"key",sz )
    print "get key ->",ret_key.decode(sz[0])
    rc = sp.destroy(ret_o)



def cursor_strkeys(sp, db, strkey, order):
    o = sp.object(db)
    szk = sp.ffi.cast("uint32_t",len(strkey) )
    sp.set(o,"order",order)
    sp.set(o,"key", strkey, szk )
    cursor = sp.cursor(db, o)
    typ = sp.type(cursor)
    print "cursor?",typ._(0)
    sz = sp.ffi.new("uint32_t*")

    o = sp.get( cursor, o )
    while o.cd != sp.ffi.NULL:
        key = sp.get(o,"key",sz)
        #ckey = sp.ffi.cast(itp,key.cd)
        print "key -> ",key.prefix(sz[0],strkey)
        o = sp.get( cursor, o )

 


sp, env, ctl  = set_nv()
set_custom_comparsion(sp, ctl)
db = open_nvdb(sp, env, ctl)


data_list = [
"az","azimut","aston","advert","abby",
"hot","hobby","hobbit","homo",
"sapiens","erectus","evidence","eon","e",
"sciense","hacking","hack"
]


for item in data_list:
    print "set in: ",item
    set_str_key( sp, db, item )

for item in data_list:
    print "get from: ",item
    get_str_key(sp,db, item )

# prefix cursor
try:
    cursor_strkeys(sp,db,"e",">=")
except StopIteration:
    print "all prefixes done"


close_nv(sp, env)
 
