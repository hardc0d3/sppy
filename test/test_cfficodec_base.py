# -*- coding: utf-8 -*-

class AlaBala(object):
    def __init__(self):
        self.name = "name"
        self.test = "test"


import sys
sys.path.append('../cfficodecs')

from cfficodec import  BaseCodec 
c = BaseCodec()

a = 999


st =  c.encode("azbuka")

print c.decode( st,len(st) )

ust =  c.encode( unicode("азбука %d" % a,"utf-8") )

r = c.decode( ust,len(ust) )

print r,r[1]

c1 = c.encode(1111)
c2 = c.encode(11111111111)
c3 = c.encode(11111111111111111111111111111)


print c.decode( c1, len(c1) )
print c.decode( c2, len(c2) )
print c.decode( c3, len(c3) )

ls = c.encode ( [1,2,3] )
lt = c.encode ( (1,11234,12341234) )
print c.decode(ls,len(ls) )
print c.decode(lt,len(lt) )



