
import sys

sys.path.append('./build/lib.linux-x86_64-2.7/')

from voidptr import VoidPtr as vp
import spapi as sp

env = vp("env")
ctl = vp("ctl")
db  = vp("db")
o = vp("o")
t = vp("t")

print "env", sp.env(env)
print "env,ctl", sp.ctl(env,ctl)
print "ctl_set", sp.ctl_set(ctl,"sophia.path","./test_data")
print "ctl_set", sp.ctl_set(ctl,"db","test_p")
print "open env", sp.open(env)
print "db", sp.db(ctl,"db.test_p",db)
print "transaction begin", sp.begin(env,t)

for j in xrange (6)
    for k in xrange(6):
        print "prepare obj" , sp.obj(db, o)

        key = "a%db%dc%d" % (k,k,k)
        print "key -> ",key

        print "set field",sp.set_field(o,"key",key )
        print "set fieled",sp.set_field(o,"value","abcd%d" % k)
        print "db set obj",sp.db_set( t, o ) 

print "transaction commit", sp.commit(t)

cursor = vp("cursor")
#cursor2 = vp("cursor2")
#o2 = vp("o2")

#print "obj db o2" , sp.obj(db, o2)
print "obj db o" , sp.obj(db, o)

print "set key ", sp.set_field(o,"key","a5")
print "set order > to o",sp.set_field(o,"order",">")
#print "set order > to o2",sp.set_field(o2,"order",">")


print "inti cursors"
print cursor.tag, sp.cursor(db,o,cursor)
#print cursor2.tag, sp.cursor(db,o2,cursor2)

while sp.cursor_get(cursor,o):
     print sp.get_field(o,"key")
     #if sp.cursor_get(cursor2,o2):
     #      print sp.get_field(o2,"key")




