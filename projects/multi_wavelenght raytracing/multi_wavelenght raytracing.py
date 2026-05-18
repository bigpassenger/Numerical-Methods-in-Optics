import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi

N = 7
y0 = np.linspace(-0.02, 0.02, N)
ti = 3
tt = ti * pi / 180
lamb = np.linspace(400e-9, 700e-9, N)
A = 1.6215
B = 0.015e-12

def n_lambda(lamb):
    return A + B / (lamb ** 2)

def get_color_name(lamb):
    lamb_nm = lamb * 1e9
    if 635 <= lamb_nm <= 700:
        return 'red'
    elif 590 <= lamb_nm < 635:
        return 'orange'
    elif 560 <= lamb_nm < 590:
        return 'yellow'
    elif 490 <= lamb_nm < 560:
        return 'green'
    elif 450 <= lamb_nm < 490:
        return 'blue'
    elif 400 <= lamb_nm < 450:
        return 'magenta'
    else:
        return 'black'

def propagate(y, theta, d):
    return y + tan(theta) * d

def transformation_matrice(y, theta, type_, n):
    if type_ == "lens":
        f = 1 / ((n - 1) * (1/R1 - 1/R2))
        M = np.array([[1, 0], [-1/f, 1]])
    elif type_ == "planar":
        n1, n2 = 1.0, n
        M = np.array([[1, 0], [0, n1/n2]])
    elif type_ == "spherical":
        n1, n2 = 1.0, n
        R = 0.05
        M = np.array([[1, 0], [(n1 - n2) / (n2 * R), n1 / n2]])

    v_in = np.array([y, theta])
    v_out = M @ v_in
    return v_out

def loop(N, y0, theta0, d1, d2, type_, n_arr):
    rays_x, rays_y = [], []
    x0 = 0.0
    for i in range(N):
        y1 = propagate(y0[i], theta0, d1)
        rays_y.append([y0[i], y1])
        rays_x.append([x0, d1])
        out = transformation_matrice(y1, theta0, type_, n_arr[i])
        y2, theta2 = out[0], out[1]
        y3 = propagate(y2, theta2, d2)
        rays_y.append([y2, y3])
        rays_x.append([d1, d1 + d2])
    return rays_x, rays_y

def plot(rays_x, rays_y, N, lamb, d1, d2, element_type):
    plt.figure(figsize=(10, 5))
    for i in range(N):
        color_name = get_color_name(lamb[i])

        plt.plot(rays_x[2*i], rays_y[2*i], 
                 color=color_name, linestyle='-', linewidth=1.2)

        plt.plot(rays_x[2*i+1], rays_y[2*i+1], 
                 color=color_name, linestyle='-', linewidth=1.2)

    
    plt.plot([d1, d1], [-0.05, 0.05], 'k--', linewidth=1, label='Lens plane')
    plt.xlim(0, d1 + d2 + 0.02)
    plt.ylim(-0.05, 0.05)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.grid(True)
    plt.legend()
    plt.title(f'Ray tracing - {element_type} (Chromatic aberration)')
    plt.savefig(f'{element_type}_chromatic_visible.png', dpi=150)
    plt.show()

# -------------------main
if __name__ == "__main__":
    n_values = np.array([n_lambda(lam) for lam in lamb])
    R1, R2 = 0.05, -0.05
    d1 = 0.08
    lambda_ref = 550e-9
    n_ref = n_lambda(lambda_ref)
    f_ref = 1 / ((n_ref - 1) * (1/R1 - 1/R2))
    d2 = f_ref   
    
    element_type = "planar"
    if element_type == "spherical":
        d2 = 0.25
    rays_x, rays_y = loop(N, y0, tt, d1, d2, element_type, n_values)
    plot(rays_x, rays_y, N, lamb, d1, d2, element_type)