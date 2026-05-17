from math import pi, tan
import numpy as np
import matplotlib.pyplot as plt

N = 20
y0 = np.linspace(-0.01, 0.01, N)
alpha = 0.005
ti = alpha * pi/180
tt = 2* alpha
R_obj = 0.030
d1 = 0.1
d2 = 0.19
d3 = 0.50
f1 = -0.15
f2 = 0.3

def propagate(y, tt, d1):
    return y + tan(tt) * d1

def lens(f, y, tt):
    v1 = np.array([y, tt])

    M = np.array([[1, 0],
                  [-1/f, 1]])
    v2 = M @ v1
    return v2
rays = []
x_ = []

for i in range(N):
    x_ray = [0]
    y_ray = [y0[i]]

    y1 = propagate(y0[i], tt, d1)
    x_ray.append(d1)
    y_ray.append(y1)

    v2 = lens(f1, y1, tt)
    y3 = propagate(v2[0], v2[1], d2)
    x_ray.append(d2)
    y_ray.append(y3)

    v4 = lens(f2, y3, v2[1])
    y5 = propagate(v4[0], v4[1], d3)
    x_ray.append(d3)
    y_ray.append(y5)

    rays.append(y_ray)
    x_.append(x_ray)


for i in range(N):
    plt.plot(x_[i], rays[i], 'b-')

plt.plot([d1,d1], [-0.1,0.1],'k--', linewidth=0.8, label='Lens1 plane')
plt.plot([d2,d2], [-0.1,0.1],'k--', linewidth=0.8, label='Lens2 plane')
plt.plot([d3, d3], [-0.1,0.1],'k--', linewidth = 0.8, label = 'objective plane')
plt.axhline(y=R_obj, color='r', linestyle='--')
plt.axhline(y=-R_obj, color='r', linestyle='--')
plt.xlim(0, d1 + d2 + d3 + 0.05)
plt.ylim(-0.1, 0.1)
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
print(f"The mirror's angel is {alpha}")
print(f"The first lens' angle is {f1}")
print(f"The second lens' angle is {f2}")
