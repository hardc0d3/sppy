import sys
sys.path.append('../cfficodecs')

from cfficodec import  CharString
import cffi
cdef = """

void free(void *);
void *malloc(size_t size);

"""
ffi = cffi.FFI()
ffi.cdef(cdef)
lib = ffi.dlopen(None)

c = CharString(ffi,lib)

cd = c.encode("test_string_obj")
print cd
st = c.decode(cd)
print st
