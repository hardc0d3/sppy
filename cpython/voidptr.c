/*
 * BSD 2 clause
 * ( C ) 2015, Dobri Stoilov dobri.stoilov at gmail.com
 */


#include "Python.h"
#include "voidptr.h"
#include "structmember.h"

static PyObject *
VoidPtr_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {

    VoidPtr *self;
    self = (VoidPtr *)type->tp_alloc(type, 0);
    if (self != NULL) {
       self->ptr = NULL;
       self->tag = PyString_FromString("");
       
       if (self->tag == NULL) {
            Py_DECREF(self);
            Py_RETURN_NONE;
       }
       return (PyObject *)self;
    }
    else {
       
       Py_RETURN_NONE;
    }

    Py_RETURN_NONE;
}


static void
VoidPtr_del(VoidPtr* self) {

    Py_XDECREF(self->tag);
    self->ob_type->tp_free((PyObject*)self);
}


static int
VoidPtr_init(VoidPtr *self, PyObject *args, PyObject *kwds) {

    int ok;
    PyObject *tag=NULL;
    self->ptr = NULL;

    ok = PyArg_ParseTuple(args, "O",&tag); 
    
    if (tag != NULL && ok) {
        Py_INCREF(tag);
        self->tag = tag;
    }

    return 0;
}


static PyObject *
VoidPtr_isnull(VoidPtr* self) {

    if( self->ptr == NULL )
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}


static PyMemberDef VoidPtr_members[] = {
    {"tag", T_OBJECT_EX, offsetof(VoidPtr, tag), 0,
     "VoidPointer tag"},
    {NULL}  /* Sentinel */
};




static PyMethodDef VoidPtr_methods[] = {
    {"isnull", (PyCFunction)VoidPtr_isnull, METH_NOARGS,
     "Return the True if void ptr is NULL"
    },
    {NULL}   //Sentinel 
}; 



static PyTypeObject VoidPtrType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "voidptr.VoidPtr",         /*tp_name*/
    sizeof(VoidPtr),           /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)VoidPtr_del,   /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "void ptr object",         /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    VoidPtr_methods,           /* tp_methods */
    VoidPtr_members,           /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)VoidPtr_init,      /* tp_init */
    0,                         /* tp_alloc */
    VoidPtr_new,                 /* tp_new */
};

static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

void initvoidptr(void)
{

    PyObject* m;


    if (PyType_Ready(&VoidPtrType) < 0)
        return;

    m = Py_InitModule3("voidptr", module_methods,
                   "voidptr py mod");
    if (m == NULL)
      return;

   Py_INCREF(&VoidPtrType);
   PyModule_AddObject(m, "VoidPtr", (PyObject *)&VoidPtrType);

}




