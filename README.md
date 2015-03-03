# sppy
sphia.org v1.2 cff binding 


status:

work in progress:
* see  test/test_cffi_wrap.py
* wrap design follows original sophia db api and workflow
* wrap and api should be dynammically combinied
* for high level abstraction see test_sophia/


first benchmark:

* set_base.py and get_base.py
* model name	: Intel(R) Core(TM) i3-3120M CPU @ 2.50GHz
* HDD
* Python 2.7.3 (default, Feb 27 2014, 19:58:35) 
* [GCC 4.6.3] on linux2
* ""
* set from 1 to 99999 numerical keys
*  9.95449280739
* set from 1 to 99999 string keys
*  20.4761548042
* env open 0
* get from 1 to 99999 numerical keys
* 11.4260380268
* get from 1 to 99999 string keys
* 10.7298150063
* pypy
* Python 2.7.8 (10f1b29a2bd2, Feb 02 2015, 21:22:43)
* [PyPy 2.5.0 with GCC 4.6.3] on linux2
* set from 1 to 99999 numerical keys
* 2.8616900444
* set from 1 to 99999 string keys
* 5.32412314415
* env open 0
* get from 1 to 99999 numerical keys
* 3.67419099808
* get from 1 to 99999 string keys
* 2.82167005539


roadmap:

* cffi method is on dev, in order to support pypy
* light & simple encoding decoding to distinguish py types in same db
