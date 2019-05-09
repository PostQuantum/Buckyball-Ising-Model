# Solving Statistical Mechanics using Variational Autoregressive Networks
Paper link: [arXiv:1809.10606](https://arxiv.org/abs/1809.10606) | [Phys. Rev. Lett. 122, 080602 (2019)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.122.080602)

The code requires Python >= 3.6 and PyTorch >= 1.0. If you have configured your PyTorch installation with a recent Nvidia GPU card, you can enjoy enormously acceleration (> 10x).

Directory `src_ising` contains code for 2D FM and AFM Ising model, and `src_hop_sk` contains code for Hopfield model, SK model and inverse Ising problem. Run `python3 src_ising/main.py --help` to see all configurations.

Script `src_ising/reproduce.sh` and `src_hop_sk/reproduce.sh` are commands to reproduce the results in Fig. 2~4. Directly running these scripts may take thousands of GPU hours, and produce hundreds GB of output data, most of which are network weights during training steps. In practice, you may run these commands in parallel on multiple GPUs, and set appropriate output path.



---

---

This program is based on Dian Wu's code. I modified its lattice structure and obtained the buckyball lattice free energy per site.



I modified the hamiltonian in file sk.py. Just a small modification.

---

---

