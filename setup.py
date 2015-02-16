from distutils.core import setup, Extension

setup(name="voidptr", version="0.0",
	ext_modules = [
         Extension(
        
         "voidptr", ["voidptr.c"],
         include_dirs=['./'], 
         #extra_objects=[''],
         #extra_compile_args=['']

      ),
         Extension(

         "spapi", ["spapi.c"],
         include_dirs=['../sophia/','./'],
         extra_objects=['../sophia/libsophia.a'],
         #extra_compile_args=['']

      )
      ]
     )

