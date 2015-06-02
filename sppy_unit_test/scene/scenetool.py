import os
import shutil

class DataScene(object):
    def __init__(self,scene_dir):
        self.scene_dir = scene_dir 
        
    def ensure(self):
        if not os.path.isdir(self.scene_dir):
            os.makedirs(self.scene_dir)

    def clean(self): 
        shutil.rmtree(self.scene_dir)


if __name__ == '__main__':

    print "test scene tool"
    scene = DataScene('../../test_data/test_scene')  
    scene.ensure()
    scene.clean()
    scene.ensure()



