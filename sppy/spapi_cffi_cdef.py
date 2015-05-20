
sophia_api_cdef = """

/*
 * sophia database API
 * sphia.org
 *
 * C API Copyright (c) Dmitry Simonenko
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


