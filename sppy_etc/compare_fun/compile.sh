rm *.pyc
rm *.o
rm *.so
gcc -g -O -fPIC -c cmp.c 
gcc -pthread -shared -Wall,-O2 cmp.o -o cmp.so

