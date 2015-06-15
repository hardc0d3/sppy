import cffi
import sp_index_cmp.cmpdef as cmpdef
from sppy.spapi_cffi_codecs import ListU32
from random import randint

ffi = cffi.FFI()
ffi.cdef ( cmpdef.cdef )
lib = ffi.dlopen("./sp_index_cmp/cmp.so")


def pycmp( a,b ):
   if a<b: return -1
   elif a>b: return 1
   else: return 0

cases = []
case_count = 100000

for i in xrange(1,case_count):
    ll1 = list([])
    ll2 = list([])
    for k in xrange(1,randint(1,10)):
        ll1.append( randint(1,100000))
    for k in xrange(1,randint(1,10)):
        ll2.append(randint(1,100000))
    cases.append([ll1,ll2])

codec =  ListU32(ffi)

for case in cases:
   l1 = case[0]
   l2 = case[1]
   cl1 = codec.encode(l1)
   cl2 = codec.encode(l2)
# compare_u32list(char *a, size_t asz, char *b, size_t bsz, void *arg)
   r = lib.compare_u32list( cl1,len(cl1),cl2,len(cl2), ffi.NULL )
   assert r == pycmp(l1,l2)
 



