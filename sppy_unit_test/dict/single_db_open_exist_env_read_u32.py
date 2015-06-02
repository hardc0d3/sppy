import unittest
import single_db_conf as conf
from scene.scenetool import DataScene
from sppy.spapi_ctl_dict import SophiaCtlDict
from sppy.spapi_dict import SophiaDict


class TestOpenExistEnvReadData(unittest.TestCase):
    
    def test_open_exist_env_read_data(self):
        sp = conf.sp
        env = sp.env()
        self.assertEqual('env',sp.type(env).decode(0) )
        ctl = sp.ctl(env)
        self.assertEqual('ctl',sp.type(ctl).decode(0) )
        u32 = conf.u32
   
        dctl = SophiaCtlDict(sp,ctl)
        dctl['sophia.path_create'] = u32.encode(0)
        dctl['sophia.path'] = conf.scene_dir
        dctl['db'] = conf.db_name
  
        rc = sp.open(env)
        self.assertEqual(0,rc.decode(0) ) 
        db = dctl['db.%s'%conf.db_name]
        self.assertEqual('database',sp.type(db).decode(0) )

        ddb = SophiaDict(conf.dict_db_conf, db )
  
        for i in xrange(conf.start,conf.stop):
            k = ddb[i]
            self.assertEqual(k,i-conf.offset)

        rc = sp.destroy(db)
        self.assertEqual(0,rc.decode(0) )

        rc = sp.destroy(env)
        self.assertEqual(0,rc.decode(0) )


if __name__ == '__main__':
    unittest.main()


