import numpy as np
import torch

class DynamicalLowRankApproximation:
    def __init__(self, rank, dim):
        self.rank = rank
        self.dim = dim
        self.U = torch.randn(dim, rank, dtype=torch.float32)
        self.S = torch.randn(rank, rank, dtype=torch.float32)
        self.V = torch.randn(dim, rank, dtype=torch.float32)
        self.orthogonalize()

    def orthogonalize(self):
        self.U, _ = torch.linalg.qr(self.U)
        self.V, _ = torch.linalg.qr(self.V)

    def project(self, A):
        return self.U @ self.S @ self.V.T

    def update(self, A, dt):
        R = A - self.project(A)
        dU = R @ self.V @ torch.linalg.inv(self.S.T)
        dV = R.T @ self.U @ torch.linalg.inv(self.S)
        dS = self.U.T @ R @ self.V

        self.U = self.U + dt * dU
        self.S = self.S + dt * dS
        self.V = self.V + dt * dV
        self.orthogonalize()

def generate_dummy_data(dim, timesteps):
    A = torch.zeros(timesteps, dim, dim, dtype=torch.float32)
    for t in range(timesteps):
        A[t] = torch.randn(dim, dim, dtype=torch.float32)
    return A

if __name__ == '__main__':
    dim = 50
    rank = 10
    timesteps = 100
    dt = 0.01

    A = generate_dummy_data(dim, timesteps)
    dlra = DynamicalLowRankApproximation(rank, dim)

    for t in range(timesteps):
        dlra.update(A[t], dt)
        reconstructed = dlra.project(A[t])
        error = torch.norm(A[t] - reconstructed) / torch.norm(A[t])
        print(f"Time step {t+1}/{timesteps}, Reconstruction Error: {error:.6f}")