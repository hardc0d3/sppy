import cffi
import sp_index_cmp.cmpdef as cmpdef
from sppy.spapi_cffi_codecs import ListU32

ffi = cffi.FFI()
ffi.cdef ( cmpdef.cdef )
lib = ffi.dlopen("./sp_index_cmp/cmp.so")


def pycmp( a,b ):
   if a<b: return -1
   elif a>b: return 1
   else: return 0



l1 = [ 3,2,1 ]
l2 = [ 3,2,1,1,1,1,1,1 ]

codec =  ListU32(ffi)


cl1 = codec.encode(l1)
cl2 = codec.encode(l2)

print cl1,len(cl1)
print cl2,len(cl2)

# compare_u32list(char *a, size_t asz, char *b, size_t bsz, void *arg)
r = lib.compare_u32list( cl1,len(cl1),cl2,len(cl2), ffi.NULL )

print r, pycmp(l1,l2)
 


# compare_function(char *a, size_t asz, char *b, size_t bsz, void *arg);
#r = lib.compare_function( ffi.new("char[]","abc"),3,ffi.new("char[]","ab"),2,ffi.new("size_t*",0) )

#print "compare abc and ab", r

#pointer = ffi.new("char[64]")

#rc = lib.print_pointer( pointer, ffi.cast("size_t",64) , lib.compare_function ) 

#print rc

#print pointer

