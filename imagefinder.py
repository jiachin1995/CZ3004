import settings

class Imagefinder:
    def find(self):
        """
        outputs results
        
        0 - left
        1 - middle
        2 - right
        """
        import numpy as np
        i = int(np.random.rand()*10)
        
        if i==0:
            j = int(np.random.rand()*4)
        else:
            j=0
            
            
        fake_results = [
            None,
            ["id", 0],
            ["id", 1],
            ["id", 2]
        ]
    
        return fake_results[j]


