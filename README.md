# sppy
sphia.org v1.2 python cffi binding 


example usage:

    from sppy import SophiaApi
    from sppy from sppy import sophia_api_cdef

    sp_dl = '../build/sp.so'
    sp = SophiaApi( sp_dl, sophia_api_cdef )

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


* Wrap object have decode method, when api function resulting integer decoder don't need data len. Decode is used when returned object is data but not handle like env, ctl, object, cursor.
* Currently api function arguments recieve 3 type variants, Wrap object that carry sophia handle types or cffi cdata, python str which is encoded to cffi cdata char*
* for detailed sophia api docs,please check with http://sphia.org/documentation.html 


