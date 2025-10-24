from biomechzoo.conversion.c3d2zoo_data import c3d2zoo_data
import matplotlib.pyplot as plt
from ezc3d import c3d
import numpy as np

def load(data: str):

    c = c3d(data)
    sample_data = c3d2zoo_data(c)

    m1 = sample_data['RightHeel1']['line']  # [2000:]
    m2 = sample_data['RightHeel2']['line']  # [2000:]
    m3 = sample_data['RightHeel3']['line']  # [2000:]
    m4 = sample_data['RightHeel4']['line']  # [2000:]

    M1 = sample_data['RightShank1']['line']  # [2000:]
    M2 = sample_data['RightShank2']['line']  # [2000:]
    M3 = sample_data['RightShank3']['line']  # [2000:]
    M4 = sample_data['RightShank4']['line']  # [2000:]

    return {
        "m1": m1, "m2": m2, "m3": m3, "m4": m4,
        "M1": M1, "M2": M2, "M3": M3, "M4": M4
    }

def unit_vector(v):
    """Returns the unit vector of a given vector."""
    norm_vector = v / np.linalg.norm(v, axis=1)[:, None]
    return norm_vector

def distal_local_cord_sys(m1, m3, m4):
    """Builds a coordinate system for the distal segment
    prints determinants - should be + 1.00 for a right-handed system"""
    i = unit_vector(m1 - m3)
    Vtemp = unit_vector(m4 - m3)
    j = unit_vector(np.cross(Vtemp, i))
    k = unit_vector(np.cross(i, j))
    rotation_matrix = np.stack((i, j, k), axis=2)  # shape: (N, 3, 3)
    determinants = np.linalg.det(rotation_matrix)
    print(f"Distal segment determinant: mean={np.mean(determinants):.2f}, "
          f"min={np.min(determinants):.2f}, max={np.max(determinants):.2f}")
    return j, k, i


def proximal_local_cord_sys(M1, M2, M3):
    """Builds a coordinate system for the proximal segment
    prints determinants - should be + 1.00 for a right-handed system """
    I = unit_vector(M3 - M1)
    Vtemp = unit_vector(M2 - M1)
    J = unit_vector(np.cross(Vtemp, I))
    K = unit_vector(np.cross(I, J))
    R = np.stack((I, J, K), axis=2)
    determinants = np.linalg.det(R)
    print(f"Proximal segment determinant: mean={np.mean(determinants):.2f}, "
          f"min={np.min(determinants):.2f}, max={np.max(determinants):.2f}")
    return J, K, I

def grood_angles(J, K, I, j, k, i):
    """Computes joint angles based on the Grood & Suntay equations"""
    N = J.shape[0]
    alpha = np.zeros(N)
    beta  = np.zeros(N)
    gamma = np.zeros(N)
    e2 = unit_vector(np.cross(i,K))
    for n in range(N):
        dot_alpha = np.dot(-e2[n], I[n])
        dot_beta  = np.dot(K[n], i[n])
        dot_gamma = np.dot(-e2[n], k[n])
        alpha[n] = -np.degrees(np.arcsin(dot_alpha))
        beta[n]  = np.degrees(np.arccos(dot_beta)-(np.pi/2)) # note the pi/2 offset removal
        gamma[n] = -np.degrees(np.arcsin(dot_gamma))
    return alpha, beta, gamma, e2

def plot(alpha, beta, gamma):

    plt.figure(figsize=(10, 8))
    time = np.arange(len(alpha))

    plt.subplot(3, 1, 1)
    plt.plot(time, alpha, label='alpha', color="red")
    plt.ylabel('Rotation (deg)')
    plt.xlabel('Frames')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(time, beta, label='beta', color='green')
    plt.ylabel('Abduction/Adduction (deg)')
    plt.xlabel('Frames')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(time, gamma, label='gamma')
    plt.ylabel('Flexion / Extension (deg)')
    plt.xlabel('Frames')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()