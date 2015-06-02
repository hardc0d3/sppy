import unittest
import single_db_conf as conf
from scene.scenetool import DataScene
from sppy.spapi_ctl_dict import SophiaCtlDict
from sppy.spapi_dict import SophiaDict


class TestCreateEnvLoadData(unittest.TestCase):
    
    def test_create_env_load_data(self):
        scene = DataScene(conf.scene_dir)
        scene.ensure()
        scene.clean()
        scene.ensure()

        sp = conf.sp
        env = sp.env()
        self.assertEqual('env',sp.type(env).decode(0) )
        ctl = sp.ctl(env)
        self.assertEqual('ctl',sp.type(ctl).decode(0) )
   
        dctl = SophiaCtlDict(sp,ctl)
        dctl['sophia.path'] = conf.scene_dir
        dctl['db'] = conf.db_name
  
        rc = sp.open(env)
        self.assertEqual(0,rc.decode(0) ) 
        db = dctl['db.%s'%conf.db_name]
        self.assertEqual('database',sp.type(db).decode(0) )

        ddb = SophiaDict(conf.dict_db_conf, db )
  
        for i in xrange(conf.start,conf.stop):
            ddb[i]=i-conf.offset

        rc = sp.destroy(db)
        self.assertEqual(0,rc.decode(0) )

        rc = sp.destroy(env)
        self.assertEqual(0,rc.decode(0) )


if __name__ == '__main__':
    unittest.main()


