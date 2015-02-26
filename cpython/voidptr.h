/*
 * BSD 2 clause
 * ( C ) 2015, Dobri Stoilov dobri.stoilov at gmail.com
 */


typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    PyObject *tag; /* first name */
    void *ptr;
} VoidPtr;





