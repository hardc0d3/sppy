
import cffi
from encdec_cffi import EncoderDecoder as ED

ffi = cffi.FFI()
ed = ED(ffi)


i = int(134123)
l = long(12341234134132)
f = float(11234.12341234132)


print "uint",i,ed.enc_unum("int",i)
print "ulong",l,ed.enc_unum("long",l)
print "double",f,ed.enc_num("double",f)





