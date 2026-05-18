import numpy as np
import matplotlib.pyplot as plt
from math import tan, pi

N = 5
y0 = np.linspace(-0.01, 0.01, N)
ti = 5
tt = ti * pi/180
lamb = np.linspace(400e-9, 700e-9, N)
# define B, A for BK7 slit, note that B is in the meter scale
B = 0.00420e-12
A = 1.5046
# define distances
d1 = 0.08
d2 = 0.25

def n_lambda(lamb):
    n_l = A + B/(lamb **2)
    return n_l

def color(lamb):
    lamb_nm = lamb * 1e9
    if 635 <= lamb_nm <= 700:
        return 'r-'
    elif 590 <= lamb_nm < 635:
        return 'orange'
    elif 560 <= lamb_nm < 590:
        return 'y-'
    elif 490 <= lamb_nm < 560:
        return 'g-'
    elif 450 <= lamb_nm < 490:
        return 'b-'
    elif 400 <= lamb_nm < 450:
        return 'm-'
    else:
        return 'k-'

def propagate(y0, tt, d):
    y = y0 + tan(tt)*d
    return y

def transformation_matrice(y0, tt, type_, n_):
    if type_ == "lens":
        f = 0.1
        M = np.array([[1, 0],
                  [-1/f, 1]])
    elif type_ == "planar":
        n1, n2 = 1.0, n_  
        M = np.array([[1, 0], [0, n1/n2]])
    elif type_ == "spherical":

        n1, n2 = 1.0, n_
        R = 0.05  
        M = np.array([[1, 0], [(n1-n2)/(n2*R), n1/n2]])

    v1 = np.array([y0, tt])
    v2 = M @ v1
    return v2

def loop(N, y0, tt, d1, d2, type_, n_):
    rays_y = []
    rays_x = []
    x0 = 0.0   
    for i in range(N):
        y1 = propagate(y0[i], tt, d1)
        rays_y.append([y0[i], y1])
        rays_x.append([x0, d1])
        y2 = transformation_matrice(y1, tt, type_, n_[i])   
        y3 = propagate(y2[0], y2[1], d2)
        rays_y.append([y2[0], y3])
        rays_x.append([d1, d1+d2])   
    return rays_x, rays_y

def plot(rays_x, rays_y, N, lamb, element_type):
    for i in range(N):
        plt.plot(rays_x[2*i], rays_y[2*i], color(lamb[i]), linewidth=1.5)
        plt.plot(rays_x[2*i+1], rays_y[2*i+1], color(lamb[i]), linewidth=1.5)

    plt.plot([d1,d1], [-0.03, 0.03], 'k--', label = 'surface')
    plt.xlim(0, d2)
    plt.ylim(-0.03, 0.03)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.grid(True)
    plt.box(True)
    plt.gca().set_title('Wavefront and rays', fontsize=14)
    plt.legend()
    plt.savefig(element_type)
    plt.show()

# --------- main 
if __name__ == "__main__":
    n_values = np.array([n_lambda(lam) for lam in lamb])
    
    element_type = "planar"
    
    f = 0.1   
    
    rays_x, rays_y = loop(N, y0, tt, d1, d2, element_type, n_values)
    

    plot(rays_x, rays_y, N, lamb, element_type)