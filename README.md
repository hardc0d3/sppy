# sppy
sphia.org v1.2 cffi python binding 

status: work in progress,but with very basic:
* low level api wrapper functionallity
* high level abstraction and test units 
* lack of documentation
* lack of packaging

notes:
* python,c data conversion is done vith codecs using cffi
* please see sppy_test as example how to use low level api wrapper
* and sppy_dict_test as example for dict interface wrapper


to do:
* impl for cursor functionality as generators and high level cursor interfaces
* improve err handling
* abstract environment ctl and db collections
* better unit tests
* abstract and add/test features from sophia 1.3
* impl additional codecs, to support python types 
* publish docs
* python packaging

