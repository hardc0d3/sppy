# -*- coding: utf-8 -*-
import sys
sys.path.append('../cfficodecs')

from cfficodec import  BaseCodec 
c = BaseCodec()

a = 999

print c.decode( c.encode("azbuka"))

r = c.decode( c.encode( unicode("азбука %d" % a,"utf-8") ) )
print r,r[1]

print c.decode( c.encode(1111) )
print c.decode( c.encode(11111111111) )
print c.decode( c.encode(11111111111111111111111111111) )



