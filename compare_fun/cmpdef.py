cdef = """
extern int
compare_function(char *a, size_t asz, char *b, size_t bsz, void *arg);

extern int 
compare_str(char *a, size_t asz, char *b, size_t bsz, void *arg);

extern int
print_pointer ( char* pointer, size_t psz, void* func);
"""
