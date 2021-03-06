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


cases = [
[[3,2],[3,2,1]],
[[3,2,1],[3,2]],
[[3,2,2],[3,2,2]],
[[3,2,1],[3,4,1]],
[[3,4,1],[3,2,1]],
[[3,4],[3,2,1,2]],
]

codec =  ListU32(ffi)

for case in cases:
   l1 = case[0]
   l2 = case[1]
   cl1 = codec.encode(l1)
   cl2 = codec.encode(l2)
# compare_u32list(char *a, size_t asz, char *b, size_t bsz, void *arg)
   r = lib.compare_u32list( cl1,len(cl1),cl2,len(cl2), ffi.NULL )
   assert r == pycmp(l1,l2)
 



