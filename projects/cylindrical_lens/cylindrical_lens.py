import numpy as np
import matplotlib.pyplot as plt
from math import pi

"""
cylindrical lens project by Amin Mottaghi 
This simple project can simulate rays transformation through a cylindrical lens 
to investigate astigmatism aberration and plotting rays in X-Z and Y-Z projection.
"""

N = 10
x0 = np.linspace(-0.01, 0.01, N)  # creating a vector on x that shows x0 points for each ray
y0 = np.linspace(-0.01, 0.01, N)  # creating a vector on y that shows y0 points for each ray
tx = 0
ty = 0
ttx = tx * pi/180 # first angel in x for each ray in radians
tty = ty * pi/180 # first angel in x for each ray in radians
fx = 0.1 # focal distance at x
fy = 0.15 # focal distance at y
d1 = 0.1
d2 = 0.2

def propagate(d):
    return np.array([[1, 0, d, 0],
                    [0, 1, 0, d],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]) # propagation matric this matric can be obtained by this assumption that each vector's angel stays constant but heights varies

cylindrical_lens_matrice = np.array([[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [-1/fx, 0, 1, 0],
                                    [0, -1/fy, 0, 1]]) # cylindrical lens matrice matric this matric can be obtained by this assumption that each vector's angel varies but heights are constant


z0 = []
z1 = []
z2 = []
z_end = []

for ix in range(N):
    for iy in range(N):
        v1 = np.array([x0[ix], y0[iy], ttx, tty])
        z0.append([v1[0], v1[1], v1[2], v1[2]]) # ray on the first plane
        v2 = propagate(d1) @ v1
        z1.append([v2[0], v2[1], v2[2], v2[2]])  # ray befor the lens
        v3 = cylindrical_lens_matrice @ v2
        z2.append([v3[0], v3[1], v3[2], v3[2]]) # ray after the lens
        v4 = propagate(d2) @ v3
        z_end.append([v4[0], v4[1], v4[2], v4[2]]) # ray on the interface plane


#--------------------------------plotting--------------------------------
fig2d, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
# X-Z projection
for i in range(len(z0)):
    z_coords = [0, d1, d1, d1+d2]
    x_coords = [z0[i][0], z1[i][0], z2[i][0], z_end[i][0]]
    ax1.plot(z_coords, x_coords, 'b-', linewidth=0.8, alpha=0.6)

z_lens = d1
z_fx = d1 + fx
z_fy = d1 + fy
ax1.axvline(z_lens, color='k', linestyle='--', label='Lens')
ax1.axvline(z_fx, color='r', linestyle=':', label=f'X focus (z={z_fx:.2f} m)')
ax1.axvline(z_fy, color='g', linestyle='-.', label=f'Y focus (z={z_fy:.2f} m)')
ax1.set_xlabel('z (m)')
ax1.set_ylabel('x (m)')
ax1.set_title('X-Z projection (focus in X)')
ax1.legend()
ax1.grid(True)
ax1.set_xlim(0, d1+d2)

# Y-Z projection
for i in range(len(z0)):
    z_coords = [0, d1, d1, d1+d2]
    y_coords = [z0[i][1], z1[i][1], z2[i][1], z_end[i][1]]
    ax2.plot(z_coords, y_coords, 'r-', linewidth=0.8, alpha=0.6)

ax2.axvline(z_lens, color='k', linestyle='--', label = 'Lens')
ax2.axvline(z_fx, color='r', linestyle=':', label='X focus')
ax2.axvline(z_fy, color='g', linestyle='-.', label=f'Y focus (z={z_fy:.2f} m)')
ax2.set_xlabel('z (m)')
ax2.set_ylabel('y (m)')
ax2.set_title('Y-Z projection (focus in Y)')
ax2.legend()
ax2.grid(True)
ax2.set_xlim(0, d1+d2)

plt.savefig('result.png')
plt.tight_layout()
plt.show()