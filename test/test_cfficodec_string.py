# -*- coding: utf-8 -*-

from encdec_cffi import EncoderDecoder as ED

ed = ED()

c = ed.enc_str("azbuka",ed._TYPE_STR)
print c
print "----" 
print ed.dec_str(c)


uni = unicode("азбука","utf-8")

print ed.dec_str(c)

cu = ed.enc_utf8(uni)

print cu


r = ed.dec_utf8(cu)

print r,r[2]


