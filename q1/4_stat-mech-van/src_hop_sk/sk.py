# SK model

import math
import pickle
import sys

import numpy as np
import torch


class SKModel():
    def __init__(self, n, beta, device, field=0, seed=0):
        self.n = n
        self.beta = beta
        self.field = field
        self.seed = seed
        if seed > 0:
            torch.manual_seed(seed)

        self.J = torch.randn([self.n, self.n]) / math.sqrt(n)
        # Symmetric matrix, zero diagonal
        self.J = torch.triu(self.J, diagonal=1)
        self.J += self.J.t()
        self.J = self.J.to(device)
        self.J.requires_grad = True

        self.c60labelEdge = np.load('c60labelEdge.npy') #The edge pair labels of c60 lattice
        self.c60labelNode = np.load('c60labelNode.npy') #The nearist-node labels of c60 lattice

        self.C_model = []

        print('SK model with n = {}, beta = {}, field = {}, seed = {}'.format(
            n, beta, field, seed))

    def exact(self):
        assert self.n <= 20

        Z = 0
        n = self.n
        J = self.J.cpu().to(torch.float64)
        beta = self.beta
        E_min = 0
        n_total = int(math.pow(2, n))

        print('Enumerating...')
        for d in range(n_total):
            s = np.binary_repr(d, width=n)
            b = np.array(list(s)).astype(np.float32)
            b[b < 0.5] = -1
            b = torch.from_numpy(b).view(n, 1).to(torch.float64)
            E = -0.5 * b.t() @ J @ b
            ###for iiii in range(100000):
            ###zhelichengxumeiyongdao    print('bbb',b.shape())
            if E < E_min:
                E_min = E
            Z += torch.exp(-beta * E)
            sys.stdout.write('\r{} / {}'.format(d, n_total))
            sys.stdout.flush()
        print()

        print('Computing...')
        self.C_model = torch.zeros([n, n]).to(torch.float64)
        for d in range(n_total):
            s = np.binary_repr(d, width=n)
            b = np.array(list(s)).astype(np.float32)
            b[b < 0.5] = -1
            b = torch.from_numpy(b).view(n, 1).to(torch.float64)
            E = -0.5 * b.t() @ J @ b
            prob = torch.exp(-beta * E) / Z
            self.C_model += b @ b.t() * prob
            sys.stdout.write('\r{} / {}'.format(d, n_total))
            sys.stdout.flush()
        print()

        # print(self.C_model)
        print(
            'Exact free energy = {:.8f}, paramagnetic free energy = {:.8f}, E_min = {:.8f}'
            .format(-torch.log(Z).item() / beta / n, -math.log(2) / beta,
                    E_min.item() / n))

    def energy(self, samples):
        """
        Compute energy of samples, samples should be of size [m, n] where n is the number of spins, m is the number of samples.
        """
        samples = samples.view(samples.shape[0], -1)
        assert samples.shape[1] == self.n
        m = samples.shape[0]
        eee=torch.zeros(m)
        ###Bad function
        for j in range(m):
            for i in range(90):
                eee[j] += samples[j][int(self.c60labelEdge[i,0])]*samples[j][int(self.c60labelEdge[i,1])]
        ###Good function

        ##################
        #return (-0.5 * ((samples @ self.J).view(m, 1, self.n) @ samples.view(
        #    m, self.n, 1)).squeeze() - self.field * torch.sum(samples, 1))
        return eee

    def J_diff(self, J):
        """
        Compute difference between true couplings and inferred couplings.
        """
        diff = self.J - J
        diff = diff * diff
        return math.sqrt(torch.mean(diff))

    def save(self):
        self.J = self.J.cpu()
        fsave_name = 'n{}b{:.2f}D{}.pickle'.format(self.n, self.beta,
                                                   self.seed)
        with open(fsave_name, 'wb') as fsave:
            pickle.dump(self, fsave)
        print('SK model is saved to', fsave_name)


if __name__ == '__main__':
    assert len(sys.argv) >= 4

    device = torch.device('cpu')
    n = int(sys.argv[1])
    beta = float(sys.argv[2])
    seed = int(sys.argv[3])
    sk = SKModel(n, beta, device, seed=seed)
    sk.exact()
    sk.save()
