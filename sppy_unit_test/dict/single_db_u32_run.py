import unittest

testmodules = [
    'single_db_create_env'
   ,'single_db_create_env_load_u32'
   ,'single_db_open_exist_env'
   ,'single_db_open_exist_env_read_u32'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)


