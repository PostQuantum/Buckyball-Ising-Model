"""
make ndy data file
"""
import numpy as np
import json
def read_txt_high(filename):
    with open(filename, 'r') as file_to_read:
        list0 = [] #文件中的第一列数据 
        list1 = [] #文件中的第二列数据 
        list2 = [] #文件中的第三列数据 
        dalist = [] #数据 
        c60node = np.zeros((60,3))
        #c60edge = np.zeros((90,2))
        while True: 
            lines = file_to_read.readline() # 整行读取数据 
            if not lines: 
                break 
            item = [i for i in lines.split()] 
            data0 = json.loads(item[0])#每行第一个值 
            data1 = json.loads(item[1])#每行第二个值 
            data2 = json.loads(item[2])#每行第二个值 
            list0.append(data0) 
            list1.append(data1) 
            list2.append(data2)
        dalist = [list0,list1,list2]
        #dalist = [list0,list1]
        for i in range(60):
            for j in range(3):
                c60node[i][j] = dalist[j][i]-1
        np.save('c60labelNode',c60node)
        #for i in range(90):
        #    for j in range(2):
        #        c60edge[i][j] = dalist[j][i]-1
        #np.save('c60labelEdge',c60edge)
    return list0,list1


#read_txt_high('C60labelEdge.dat')
#c = np.load('c60labelEdge.npy')
read_txt_high('C60labelNode.dat')
c = np.load('c60labelNode.npy')
print('c=',c)
print('check', c[0,0]==9)
