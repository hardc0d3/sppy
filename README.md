# sppy
sphia.org v1.2 python cffi binding 


example usage:

    from _spapi_cffi import SpApiFFI
    sp_dl = '../build/sp.so'
    sp = SpApiFFI( sp_dl )

    # env, ctl are wrap object

    env = sp.env()
    ctl = sp.ctl(env)
    rc = sp.set( ctl, "sophia.path", "../test_data/" )
    rc = sp.set( ctl, "db", "spwrap" )
    print rc.decode(0)
    # or 
    print rc._(0)
    db = sp.get( ctl, "db.spwrap" )
    rc = sp.open( env )
    skey = marshal.dumps(key)
    o = sp.object( db )
    szk = sp.ffi.cast("uint32_t",len(skey))
    rc = sp.set(o, "key",skey, szk )
    rc = sp.set(db, o)
    #. . . 
    val = sp.get(o,"value",sz)


* Wrap object have decode method, in case of "rc" with resulting integer decoder don't need data len. Decode is used when returned object is not handle like env, ctl, object, cursor
* As api function arguments, there are 3 type variants, Wrap that carry sophia handle, python str which is encoded to char* or cffi cdata. 
* test_api/test_wrap.py is example how to use cffi api wrapper
* for detailed sophia api docs, http://sphia.org/documentation.html 
* Currently lack of high level abstraction, and need help with more test cases to cover the api.


