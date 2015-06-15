
import cffi
import cmpdef

ffi = cffi.FFI()
ffi.cdef ( cmpdef.cdef )


lib = ffi.dlopen("./cmp.so")

# compare_function(char *a, size_t asz, char *b, size_t bsz, void *arg);
r = lib.compare_function( ffi.new("char[]","abc"),3,ffi.new("char[]","ab"),2,ffi.new("size_t*",0) )

print "compare abc and ab", r

pointer = ffi.new("char[64]")

rc = lib.print_pointer( pointer, ffi.cast("size_t",64) , lib.compare_function ) 

print rc

print pointer

