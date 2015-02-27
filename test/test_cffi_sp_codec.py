# -*- coding: utf-8 -*-
import sys
sys.path.append('../cfficodecs')

from cfficodec import  BaseCodec
enco = BaseCodec()


from cffi import FFI

cdef = """

/*
 * sophia database API
 * sphia.org
 *
 * Copyright (c) Dmitry Simonenko
 * BSD License
 */

void *sp_env(void);
void *sp_ctl(void*, ...);
void *sp_object(void*, ...);
int   sp_open(void*, ...);
int   sp_destroy(void*, ...);
int   sp_error(void*, ...);
int   sp_set(void*, ...);
void *sp_get(void*, ...);
int   sp_delete(void*, ...);
int   sp_drop(void*, ...);
void *sp_begin(void*, ...);
int   sp_prepare(void*, ...);
int   sp_commit(void*, ...);
void *sp_cursor(void*, ...);
void *sp_type(void*, ...);
"""

ffi = FFI()
ffi.cdef(cdef)
c = ffi.dlopen('../build/sp.so')

def _( s ):
    global ffi
    return ffi.new("char []",s)

from ctypes import cdll, Structure, c_int, c_double, c_uint

def u32t( i ):
    global ffi
    return ffi.new("int *",i)


env = c.sp_env( )
ctl = c.sp_ctl( env )
c.sp_set( ctl, _("sophia.path"), _("../test_data") )
c.sp_set( ctl, _("db"), _("test_cffi_codec") )
db = c.sp_get( ctl, _("db.test_cffi_codec") )
print "open db", c.sp_open ( env )

o = c.sp_object(db);
key = "thekey"
value = "thevalue"

count = 10

for i in xrange(count):
    o = c.sp_object(db);
    #key = _( "00%d" % i )
    #value = _( "11%d" % i )
   
    key = enco.encode( i )
    #value = enco.encode( u"буква номер %d" % i )
    value = enco.encode( (i,i+10,i+100,i+1000) )
    szk = ffi.cast("int ",ffi.sizeof(key ) )
    szv = ffi.cast("int ",ffi.sizeof(value ) ) 

    print c.sp_set(o, _("key"),key  , szk  ) 
    print c.sp_set(o, _("value"),value, szv )  
    print "dbset",c.sp_set(db, o)
    print "free", c.sp_destroy(o)


for i in xrange(count):
    o = c.sp_object(db);
    key = enco.encode( i )
    szk = ffi.cast("int ",ffi.sizeof(key ) )
    vsz = ffi.new("int *", 0 )
    ksz = ffi.new("int *", 0 )
    #szv = ffi.cast("int ",ffi.sizeof(value ) )

    print c.sp_set(o, _("key"),key  , szk  )
    r = c.sp_get(db, o) 
    val = c.sp_get(r,_("value"), vsz )
    t = enco.decode(val,vsz[0])
    print vsz[0]
    print i,"->",t[0],t[1]



print "close env", c.sp_destroy(env)



