
import numpy as np
from monte_carlo_function import Markov_chain
import os
from pylab import *

def save_image(image, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    imshow(image.reshape((28, 28)), cmap=cm.gray)
    axis('off')
    savefig(directory + os.sep + filename)

def save_data(data1, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    data_name = directory + os.sep +"datax"
    np.save(data_name, data1)

if __name__ == '__main__':
    Tem = 2
    num = 70000
    dim = 28

    x = Markov_chain(num, Tem, dim)
    save_data(x, "IsingData")
    for i in range(x.shape[0]):
        save_image(x[i], 'IsingFig', 'Fig_'+str(i)+'_original.png')

