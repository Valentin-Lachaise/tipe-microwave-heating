"""Plot of the squared Bessel functions J_n(kr)^2.

The temperature profile measured with the thermal camera is proportional to
the dissipated power, i.e. to |E|^2. For a sphere the field follows J_0(kr),
for a thick cylinder J_{-2}(kr)/r, so the heating profile is compared with the
square of these Bessel functions (see docs/images/08_validation_spheres.png and
docs/images/09_validation_cylindre_epais.png).

Annex of the TIPE slides (slide 26): "code to plot the square of Bessel
functions".
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import jn


def trace_Bessel_carre(n, xmax):
    """Plot J_n(kr)^2 for kr between 0.01 and xmax."""
    x = np.linspace(0.01, xmax, 500)
    y = (jn(n, x)) ** 2

    plt.plot(x, y, label=rf"$J_{{{n}}}(kr)^2$")
    plt.title(rf"Graphe de $J_{{{n}}}(kr)^2$")
    plt.xlabel("kr")
    plt.ylabel(rf"$J_{{{n}}}(kr)^2$")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    trace_Bessel_carre(0, 15)
