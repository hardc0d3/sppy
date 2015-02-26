
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
print "ctl_set", sp.ctl_set(ctl,"db","test_cffi")
print "open env", sp.open(env)
print "db", sp.db(ctl,"db.test_cffi",db)


cursor = vp("cursor")

print "obj db o" , sp.obj(db, o)
print "set order < to o",sp.set_field(o,"order","<")


print "inti cursors"
print cursor.tag, sp.cursor(db,o,cursor)

while sp.cursor_get(cursor,o):
     print sp.get_field(o,"key"), sp.get_field(o,"value")




