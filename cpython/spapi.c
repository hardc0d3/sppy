/*
 * BSD 2 clause
 * ( C ) 2015, Dobri Stoilov dobri.stoilov at gmail.com
 */



#include <string.h>
#include <Python.h>
#include <sophia.h>
#include "voidptr.h"


static int check_type(PyObject *o){
   /* voidptr.VoidPtr tune up how many to check*/ 
   return strncmp( "voidptr",o->ob_type->tp_name,4) != 0; 
}

static VoidPtr* get_pointer( PyObject *o ) {

    if(o == NULL || check_type(o) )  {
        return NULL;
    } else {
        return (VoidPtr*)o;
    }
}


/*
 *  (env) init env 
 */

static PyObject* spapi_env(PyObject* self, PyObject *args) {

    VoidPtr *env= NULL;
    PyObject  *o= NULL;
    if (!PyArg_ParseTuple(args, "O", &o)) {

        Py_RETURN_FALSE;
    }
    env = get_pointer(o);
    if( env != NULL ) {     
        env->ptr = sp_env();
        if ( env->ptr != NULL ) {
            Py_RETURN_TRUE;
        }
    }
    Py_RETURN_FALSE;
}

/*
 * destroy( obj | db | env | ctl | cursor ) free object do not del data 
 * return -> err code , 0 OK -1 not
 */

static PyObject* spapi_destroy(PyObject* self, PyObject *args)
{
    VoidPtr *vp=NULL;
    PyObject *pyret = Py_BuildValue("i",-1);
    PyObject  *o= NULL;
    if (!PyArg_ParseTuple(args, "O", &o)) {

        Py_RETURN_FALSE;
    }
    vp = get_pointer( o );
    if ( vp == NULL ) {
        return pyret; 
    }
    if ( vp->ptr != NULL ) {
        int ret = sp_destroy(vp->ptr);
        return Py_BuildValue("i",ret);
    }
    return pyret; 
}

/*
 * ctl( env , ctl <- ref ) -> true ok, false
 */

static PyObject* spapi_ctl(PyObject* self, PyObject *args) {

    PyObject *env= NULL;
    PyObject *ctl= NULL;
    VoidPtr *penv=NULL;
    VoidPtr *pctl=NULL;

    if (!PyArg_ParseTuple(args, "OO", &env, &ctl)) {
         Py_RETURN_FALSE;
    }
    penv = get_pointer(env);
    pctl = get_pointer(ctl);
    if ( penv != NULL  && pctl != NULL ) {
        /* do we need to chec pctl->ptr is null  */
        pctl->ptr = sp_ctl(penv->ptr);
        if ( pctl->ptr != NULL ) {

            Py_RETURN_TRUE;
        }
    }
    Py_RETURN_FALSE;
}       

/*  
 * clt_set ( ctl, string, string ) -> -1,0
 */

static PyObject* spapi_ctl_set(PyObject* self, PyObject *args) {
    VoidPtr *pctl = NULL;
    PyObject *ctl = NULL;
    char *key = NULL;
    char *val = NULL;
    PyObject *pyret = Py_BuildValue("i",-1);    

    if (!PyArg_ParseTuple(args, "Oss", &ctl,&key,&val)) {
         return pyret;
    }

    pctl = get_pointer(ctl);

    if(ctl == NULL || key == NULL || val == NULL) {

        return  pyret;
    }

    if ( pctl->ptr != NULL  ) {

       int ret = sp_set(pctl->ptr,key,val);
       return Py_BuildValue("i",ret); 
    }

    return pyret;
}

/*
 * open ( env | db ) -> -1,0=ok
 */

static PyObject* spapi_open(PyObject* self, PyObject *args){

    VoidPtr *vp=NULL;
    PyObject *o=NULL;
    PyObject *pyret= Py_BuildValue("i",-1);
    if (!PyArg_ParseTuple(args, "O", &o)) {
        
        return pyret;
    }
    vp = get_pointer( o );
    if ( vp == NULL ) {
        return pyret;
    }
    if ( vp->ptr != NULL ) {
        int ret = sp_open(vp->ptr);
        return Py_BuildValue("i",ret);
    }
    return pyret; 
}

/*
 * ( env ) -> -1?, 0,1 check environment for error
 */

static PyObject* spapi_error(PyObject* self, PyObject *args){

    VoidPtr *vp=NULL;
    PyObject *o=NULL;
    PyObject *pyret= Py_BuildValue("i",-1);
    if (!PyArg_ParseTuple(args, "O", &o)) {

        return pyret;
    }
    vp = get_pointer( o );
    if ( vp == NULL ) {
        return pyret;
    }
    if ( vp->ptr != NULL ) {
        int ret = sp_error(vp->ptr);
        return Py_BuildValue("i",ret);
    }
    return pyret;
}

/*
 * (snapshot or db ) -> -1,0=success close db 
 */

static PyObject* spapi_drop(PyObject* self, PyObject *args){

    VoidPtr *vp=NULL;
    PyObject *o=NULL;
    PyObject *pyret= Py_BuildValue("i",-1);
    if (!PyArg_ParseTuple(args, "O", &o)) {

        return pyret;
    }
    vp = get_pointer( o );
    if ( vp == NULL ) {
        return pyret;
    }
    if ( vp->ptr != NULL ) {
        int ret = sp_drop(vp->ptr);
        return Py_BuildValue("i",ret);
    }
    return pyret;
}

/*
 *  select db  ( ctl, "db.name", db ) 
 */

static PyObject* spapi_db(PyObject* self, PyObject *args) {

 VoidPtr *pobj = NULL;
 VoidPtr *pctl = NULL;
 PyObject *obj = NULL;
 PyObject *ctl = NULL;
 char *key     = NULL;

    if (!PyArg_ParseTuple(args, "OsO", &ctl,&key,&obj)) {
         Py_RETURN_FALSE;
    }

    if(ctl == NULL || key == NULL || obj == NULL) {

        Py_RETURN_FALSE;
    }
    
    pobj = get_pointer ( obj );
    pctl = get_pointer ( ctl );
    
    if ( pctl == NULL ) {
        Py_RETURN_FALSE;
    }
    // !!!
    if ( pctl->ptr != NULL  && pobj->ptr == NULL ) {

        pobj->ptr = sp_get(pctl->ptr,key);
        if( pobj->ptr != NULL ) { 
        
             Py_RETURN_TRUE;
        }
    }

Py_RETURN_FALSE;
}

/*
 * object consist as field key, values
 *  ( obj, "key" ) -> pythin string
 * to-do: pass external encoder here 
 *
 */

static PyObject* spapi_get_field(PyObject* self, PyObject *args) {
    VoidPtr *p = NULL;
    PyObject *o= NULL;
    char *f = NULL;
    //uint32_t size = 0;

    if (!PyArg_ParseTuple(args, "Os", &o,&f)) {
         Py_RETURN_NONE;
    }

    p = get_pointer ( o );
    if ( p == NULL ) {  Py_RETURN_NONE; }
    if ( p->ptr == NULL  ) {  Py_RETURN_NONE; }
    uint32_t sz;
    char *f_v  = NULL; 
    f_v  = (char*)sp_get(p->ptr, f, &sz);
    if ( f_v != NULL ) {
      
         return Py_BuildValue("s#",f_v, sz);
    }
    Py_RETURN_NONE;
}

/*
 * ( pointer ) - > "typename"
 */

static PyObject* spapi_type(PyObject* self, PyObject *args) {
    VoidPtr *p = NULL;
    PyObject *o = NULL;

    if (!PyArg_ParseTuple(args, "O", &o)) {
         Py_RETURN_NONE;
    }

    p = get_pointer ( o );
    if ( p == NULL ) { Py_RETURN_NONE; }
    if ( p->ptr == NULL  ) { Py_RETURN_NONE; }

    char *type_str  = NULL;
    type_str = (char*)sp_type(p->ptr);

    if ( type_str != NULL ) {
      return Py_BuildValue("s",type_str);
    }
    Py_RETURN_NONE;
}

/*
 * ( db,obj ) prepare object for db 
 */

static PyObject* spapi_obj( PyObject* self, PyObject *args) {
    VoidPtr *pdb = NULL;
    VoidPtr *pobj = NULL;
    PyObject *db = NULL;
    PyObject *obj = NULL;

    if (!PyArg_ParseTuple(args, "OO", &db, &obj)) {
         Py_RETURN_FALSE;
    }

    if(db == NULL || obj == NULL) {

        Py_RETURN_FALSE;
    }

    pdb = get_pointer( db );
    pobj = get_pointer( obj );

    if ( pdb == NULL || pobj == NULL ) {  Py_RETURN_FALSE; }
    if ( pdb->ptr == NULL ) { Py_RETURN_FALSE; }
    
    pobj->ptr = sp_object(pdb->ptr);
    if( pobj->ptr == NULL ) { Py_RETURN_FALSE; }

Py_RETURN_TRUE;
}

/*
 * ( o,"field key","val" ) 
 * to do: pass external decoder here
 */

static PyObject* spapi_set_field(PyObject* self, PyObject *args) {
    VoidPtr *pobj = NULL;
    PyObject *obj = NULL;
    char *field = NULL;
    char *field_value = NULL;
    //uint32_t size = 0;
    int isz=0;
    PyObject *pyret = Py_BuildValue("i",-1);

    if (!PyArg_ParseTuple(args, "Oss#", &obj,&field,&field_value,&isz) ) {
         return pyret;
    }

    if(obj == NULL || field == NULL || field_value == NULL || isz == 0) {

        return pyret;
    }
     
    pobj = get_pointer( obj );

    if ( pobj == NULL  ) { return pyret; }
    if ( pobj->ptr == NULL ) { return pyret; }

    uint32_t usz = (uint32_t) isz;
    int ret = sp_set(pobj->ptr, field, field_value,usz );

    return Py_BuildValue("i",ret);
}

/*
 * ( db or transaction, object ) transactional set -> 0 ok, -1 err
 */

static PyObject* spapi_db_set( PyObject* self, PyObject *args) {
    VoidPtr *pdb = NULL;
    VoidPtr *pobj = NULL;
    PyObject *db = NULL;
    PyObject *obj = NULL;
    PyObject *pyret = Py_BuildValue("i",-1);

    if (!PyArg_ParseTuple(args, "OO", &db, &obj)) {
         return pyret;
    }
    if(db == NULL || obj == NULL) { return pyret; }

    pdb = get_pointer( db );
    pobj = get_pointer( obj );
   
    if ( pdb == NULL || pobj == NULL ) { return pyret; }
    if ( pdb->ptr == NULL || pobj->ptr == NULL ) { return pyret; }
    int ret = sp_set(pdb->ptr, pobj->ptr);
    return Py_BuildValue("i",ret);
}

/*
 *  todo: again decoder needed
 *  ( db, object, return_value  )
 */
static PyObject* spapi_db_get( PyObject* self, PyObject *args) {
    VoidPtr *pdb = NULL;
    VoidPtr *pobj = NULL;
    VoidPtr *pret = NULL;
    PyObject *db = NULL;
    PyObject *obj = NULL;
    PyObject *ret = NULL;
    if ( !PyArg_ParseTuple(args, "OOO", &db, &obj, &ret) ) {
         Py_RETURN_FALSE;
    }
    if(db == NULL || obj == NULL || ret == NULL) {
        Py_RETURN_FALSE;
    }

    pdb = get_pointer( db );
    pobj = get_pointer( obj );
    pret = get_pointer( ret );
    
    if ( pdb == NULL || pobj == NULL || pret == NULL ) { Py_RETURN_FALSE; }
    if ( pdb->ptr == NULL || pobj->ptr == NULL || pret->ptr != NULL ) {  Py_RETURN_FALSE; }
    
    pret->ptr = sp_get(pdb->ptr, pobj->ptr);
    
    if ( pret->ptr != NULL ) { Py_RETURN_TRUE; }
    Py_RETURN_FALSE;
}


/*
 *  ( db, object, cursor) 
 * object config cursor
 */


static PyObject* spapi_cursor( PyObject* self, PyObject *args) {
    VoidPtr *pdb = NULL;
    VoidPtr *pobj = NULL;
    VoidPtr *pcursor = NULL;
    PyObject *db = NULL;
    PyObject *obj = NULL;
    PyObject *cursor = NULL;

    if (!PyArg_ParseTuple(args, "OOO", &db, &obj, &cursor)) {
         Py_RETURN_FALSE;
    }
    if(db == NULL ||  obj == NULL || cursor == NULL) { Py_RETURN_FALSE; }
  
    pdb = get_pointer( db );
    pobj = get_pointer( obj );
    pcursor = get_pointer ( cursor ) ;

    if ( pdb == NULL || pobj==NULL || pcursor == NULL ) { Py_RETURN_FALSE; }
    if( pdb->ptr == NULL  || pobj->ptr == NULL || pcursor->ptr != NULL) {  Py_RETURN_FALSE; }
    
    pcursor->ptr = sp_cursor(pdb->ptr, pobj->ptr);
    if(pcursor->ptr !=NULL) { Py_RETURN_TRUE; }

    Py_RETURN_FALSE;
}

/*
 * get current object from cursor
 * ( cursor, object ) 
 */

static PyObject* spapi_cursor_get( PyObject* self, PyObject *args) {
    VoidPtr *pc = NULL;
    VoidPtr *po = NULL;
    PyObject *c = NULL; // cursor
    PyObject *o = NULL; // object 
    if ( !PyArg_ParseTuple(args, "OO", &c, &o) ) {
         Py_RETURN_FALSE;
    }
    pc = get_pointer ( c ) ;
    po = get_pointer ( o ) ;
    if ( pc == NULL || po == NULL ) {  Py_RETURN_FALSE; }
    if ( pc->ptr == NULL || po->ptr == NULL ) {  Py_RETURN_FALSE; }
    po->ptr = sp_get( pc->ptr );
    if ( po->ptr ) {  Py_RETURN_TRUE; }
    Py_RETURN_FALSE;
}

/*
 * begin multy statement transaction
 * ( environment, transaction ) 
 */ 

static PyObject* spapi_begin( PyObject* self, PyObject *args) {
    VoidPtr *pt = NULL;
    VoidPtr *pe = NULL;
    PyObject *t = NULL; // transaction
    PyObject *e = NULL; // environment
    //pt->ptr = sp_begin( pe->ptr );
    if ( !PyArg_ParseTuple(args, "OO", &e, &t) ) {
         Py_RETURN_FALSE;
    }
    pt = get_pointer ( t ) ;
    pe = get_pointer ( e ) ;
    if ( pt == NULL || pe == NULL ) {  Py_RETURN_FALSE; }
    if ( pe->ptr == NULL ) {  Py_RETURN_FALSE; }
    pt->ptr = sp_begin( pe->ptr );
    if ( pt->ptr ) {  Py_RETURN_TRUE; }
    Py_RETURN_FALSE;
}

/*
 * ( db or transaction, object )
 * common delete operation
 */

static PyObject* spapi_delete( PyObject* self, PyObject *args) {
    VoidPtr *pd; // db or transaction 
    VoidPtr *po;
    PyObject *d = NULL;
    PyObject *o = NULL;
 
    PyObject *pyret = Py_BuildValue("i",-1);

    if (!PyArg_ParseTuple(args, "OO",  &d, &o)) {

         return pyret;
    }
    pd  = get_pointer( d );
    po  = get_pointer( o );
    
    if( pd == NULL || po == NULL ) { return pyret; }
    if( pd->ptr == NULL || po-> ptr == NULL ) { return pyret; }

    int ret = sp_delete(pd->ptr,po->ptr);
    return Py_BuildValue("i",ret);    

}

/*
 * ( transaction ) 
 * commit multy statement transaction
 */


static PyObject* spapi_commit( PyObject* self, PyObject *args) {
    VoidPtr *ptrans;
    PyObject *trans = NULL;
    PyObject *pyret = Py_BuildValue("i",-1);
    
    if (!PyArg_ParseTuple(args, "O",  &trans)) {
    
         return pyret;
    }
    ptrans = get_pointer( trans );
    if( ptrans->ptr != NULL ) { 
       
         int ret = sp_commit(ptrans->ptr);
         return Py_BuildValue("i",ret);
     }
    return pyret;
}


static PyMethodDef spapi_funcs[] = {
    //{"env", (PyCFunction)spapi_env,METH_NOARGS, NULL},
    {"env", spapi_env, METH_VARARGS, NULL }, 
    {"destroy",spapi_destroy, METH_VARARGS, NULL },
    {"ctl",spapi_ctl, METH_VARARGS, NULL },
    {"ctl_set",spapi_ctl_set, METH_VARARGS, NULL },
    {"open",spapi_open, METH_VARARGS, NULL },
    {"db",spapi_db, METH_VARARGS, NULL },
    {"get_field",spapi_get_field, METH_VARARGS, NULL },
    {"obj",spapi_obj, METH_VARARGS, NULL },
    {"set_field",spapi_set_field, METH_VARARGS, NULL },
    {"db_set",spapi_db_set, METH_VARARGS, NULL },
    {"db_get",spapi_db_get, METH_VARARGS, NULL },
    {"cursor",spapi_cursor, METH_VARARGS, NULL },
    {"cursor_get",spapi_cursor_get, METH_VARARGS, NULL },
    {"begin",spapi_begin, METH_VARARGS, NULL },
    {"commit",spapi_commit, METH_VARARGS, NULL },
    {"error",spapi_error, METH_VARARGS,NULL },
    {"drop",spapi_drop, METH_VARARGS,NULL },
    {"delete",spapi_delete, METH_VARARGS,NULL },
    {"sptype",spapi_type, METH_VARARGS,NULL },
    {NULL}
};


void initspapi(void)
{
    Py_InitModule3("spapi", spapi_funcs,
                   "spapi module");
}





