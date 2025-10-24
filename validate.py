
# Code which validates my calculations against the openOFM


import numpy as np
import matplotlib.pyplot as plt
from mocap_functions import load, distal_local_cord_sys, proximal_local_cord_sys, grood_angles
import sys

sys.path.append('/Users/joshualowery/Documents/GitHub/openOFM/python')

from linear_algebra.linear_algebra import makeunit, create_lcs, angle
from OFM.kinematics import makeax

def plot_axes_comparison(frames, ofm_axes, my_axes, axis_labels):
    """
    Plot comparison between OFM and my axes or angles.
    """
    colors = ['r', 'g', 'b']
    comp_labels = ['X', 'Y', 'Z']

    for ofm_axis, my_axis, axis_label in zip(ofm_axes, my_axes, axis_labels):
        plt.figure(figsize=(10, 5))

        if ofm_axis.ndim == 1:
            plt.plot(frames, ofm_axis, '--', color='r', label=f'OFM {axis_label}')
            plt.plot(frames, my_axis, color='r', alpha=0.7, label=f'My {axis_label}')
        else:
            for i, color in enumerate(colors):
                plt.plot(frames, ofm_axis[:, i], '--', color=color, label=f'OFM {comp_labels[i]}')
                plt.plot(frames, my_axis[:, i], color=color, alpha=0.7, label=f'My {comp_labels[i]}')

        plt.xlabel('Frames')
        plt.ylabel(axis_label + ' (unit vector components)')
        plt.title(f'{axis_label} Comparison')
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":

    dist_axis_labels = ['Distal X-axis', 'Distal Y-axis', 'Distal Z-axis']
    prox_axis_labels = ['Proximal X-axis', 'Proximal Y-axis', 'Proximal Z-axis']
    float_axis_labels = ['Float X-axis', 'Float Y-axis', 'Float Z-axis']

    ##### My workflow #####

    # Load data
    data = load('/Users/joshualowery/Desktop/EDKP_616/Section_1_Optical_MoCap/data/dynamic01.c3d')

    # Build my proximal and distal axes using my own method
    J, K, I = proximal_local_cord_sys(data['M1'], data['M2'], data['M3'])
    j, k, i = distal_local_cord_sys(data['m1'], data['m3'], data['m4'])

    my_prox_axes = [I, J, K]
    my_dist_axes = [i, j, k]

    alpha, beta, gamma, e2 = grood_angles(J, K, I, j, k, i)

    ##### OFM Workflow #####

    O_all_prox, x_all_prox, y_all_prox, z_all_prox = [], [], [], []
    O_all_dist, x_all_dist, y_all_dist, z_all_dist = [], [], [], []

    order = 'xyz' # the order that you define your axes

    # proximal coordinate system

    for n in range(data['M1'].shape[0]):
        o = data['M1'][n, :]
        axis_1 = data['M3'][n, :] - data['M1'][n, :]
        axis_2 = data['M2'][n, :] - data['M1'][n, :]
        O, lcs1, lcs2, lcs3, prox_axes_single = create_lcs(o, axis_1, axis_2, order)
        O_all_prox.append(O)
        x_all_prox.append(prox_axes_single[0])
        y_all_prox.append(prox_axes_single[1])
        z_all_prox.append(prox_axes_single[2])

    # distal coordinate system
    for n in range(data['m1'].shape[0]):
        o = data['m3'][n, :]
        axis_1 = data['m1'][n, :] - data['m3'][n, :]
        axis_2 = data['m4'][n, :] - data['m3'][n, :]
        O, lcs1, lcs2, lcs3, dist_axes_single = create_lcs(o, axis_1, axis_2, order)
        O_all_dist.append(O)
        x_all_dist.append(dist_axes_single[0])
        y_all_dist.append(dist_axes_single[1])
        z_all_dist.append(dist_axes_single[2])

    x_all_prox = np.array(x_all_prox)
    y_all_prox = np.array(y_all_prox)
    z_all_prox = np.array(z_all_prox)
    x_all_dist = np.array(x_all_dist)
    y_all_dist = np.array(y_all_dist)
    z_all_dist = np.array(z_all_dist)

    prox_axes_system = np.stack((x_all_prox, y_all_prox, z_all_prox), axis=1)
    dist_axes_system = np.stack((x_all_dist, y_all_dist, z_all_dist), axis=1)

    # putting through makeax to define the axis system according to OFM
    floatax, _, prox_x, dist_x, prox_y, dist_y, prox_z, dist_z = makeax(prox_axes_system, dist_axes_system)

    # converting to np.array
    x_all_prox, y_all_prox, z_all_prox = np.array(x_all_prox), np.array(y_all_prox), np.array(z_all_prox)
    x_all_dist, y_all_dist, z_all_dist = np.array(x_all_dist), np.array(y_all_dist), np.array(z_all_dist)

    prox_axes = [x_all_prox, y_all_prox, z_all_prox]
    dist_axes = [x_all_dist, y_all_dist, z_all_dist]

    frames = np.arange(I.shape[0])

    plot_axes_comparison(frames, prox_axes, my_prox_axes, prox_axis_labels)
    plot_axes_comparison(frames, dist_axes, my_dist_axes, dist_axis_labels)
    plot_axes_comparison(frames, [floatax[:, 0], floatax[:, 1], floatax[:, 2]],
                         [e2[:, 0], e2[:, 1], e2[:, 2]], float_axis_labels)

    # OFM calculation of resulting angles
    alpha_ofm = angle(floatax, prox_x)
    beta_ofm = -angle(prox_z, dist_x)
    gamma_ofm = angle(floatax, dist_z)

    # plotting the angle comparisons between methods
    my_angles = [alpha, beta, gamma]
    ofm_angles = [alpha_ofm, beta_ofm, gamma_ofm]
    angle_labels = ['Alpha', 'Beta', 'Gamma']

    plot_axes_comparison(frames, ofm_angles, my_angles, angle_labels)
