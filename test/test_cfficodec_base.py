# -*- coding: utf-8 -*-
import sys
sys.path.append('../cfficodecs')

from cfficodec import  BaseCodec 
c = BaseCodec()


print c.decode( c.encode("azbuka"))
r = c.decode( c.encode( unicode("азбука","utf-8") ) )
print r,r[2]
print c.decode( c.encode(1111) )
print c.decode( c.encode(11111111111) )
print c.decode( c.encode(11111111111111111111111111111) )



