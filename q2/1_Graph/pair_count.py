import numpy as np

def count(LM):
    co = 0
    if LM.shape[0]>2:
        index = np.argwhere(LM==1)[:5]
        for it in index:
            lm_ = np.delete(LM,it[0],0)
            lm_ = np.delete(lm_,it[1]-1,0)
            lm_ = np.delete(lm_,it[0],1)
            lm = np.delete(lm_,it[1]-1,1)
        
            LM[it[0],it[1]] = 0
            LM[it[1],it[0]] = 0
        
            co += count(lm)
    
    elif LM.shape[0]==2:
        if LM[0,0]==0 and LM[1,1]==0 and LM[0,1]==1 and LM[1,0]==1:
            co = 1
        else:
            co = 0
    
    return co

if __name__ == "__main__":
    LMn = [[0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0], 
          [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1], 
          [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0], 
          [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1], 
          [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0], 
          [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1], 
          [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0], 
          [0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1], 
          [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0], 
          [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1], 
          [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0], 
          [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]]
    
    LMn = np.array(LMn)
    print("pair_count = ",count(LMn))
