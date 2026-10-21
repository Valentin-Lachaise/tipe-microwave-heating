"""Variation of internal energy of a heated, axisymmetric water-like sample.

The thermal camera image is converted to temperatures (affine law between the
darkest and brightest grey levels, see temperature_profile.py). Each pixel at
column j is then treated as a thin ring of radius r = j * x and of section
x * y, so that the energy stored in the sample is

    U = sum over pixels of  c_eau * (T - Tmin) * (2 * pi * r) * (x * y) * rho_eau

As in the original script, the radius is measured from the left edge of the
image. Water properties are used for the agar-agar sample (its physical
properties are close to those of water).

Annex of the TIPE slides (slide 28): "code to compute the internal energy
variation in the ellipsoid". The pixel loops are vectorised with numpy; the
formula is unchanged. The results of this study are summarised in
docs/images/11_etude_energetique.png.

Usage:
    python internal_energy.py image.jpg --tmin 20 --tmax 60 --width 0.03 --height 0.1
"""
import argparse

import numpy as np
from PIL import Image

C_EAU = 4.18e3  # J.kg^-1.K^-1
RHO_EAU = 1000  # kg.m^-3


def variation_energie_interne(image, tmin, tmax, larg, long):
    """Return the internal energy variation (J) of the sample on the image.

    image      : PIL image of the thermal camera picture
    tmin, tmax : temperatures (deg C) at the bottom/top of the colour scale
    larg, long : real width and length of the photo, in metres
    """
    matimage = np.array(image)
    L, C = matimage.shape[0], matimage.shape[1]
    x = larg / C  # real width of one pixel (m)
    y = long / L  # real length of one pixel (m)

    # grey image: mean of the first two colour channels
    gris = (matimage[:, :, 0].astype(float) / 2 + matimage[:, :, 1].astype(float) / 2).astype(
        np.uint8
    )
    cmin, cmax = int(gris.min()), int(gris.max())
    if cmax == cmin:
        raise ValueError("The image is uniform: cannot calibrate the temperature scale.")

    # affine law T(grey) = a * grey + b with T(cmax) = tmax and T(cmin) = tmin
    a = (tmax - tmin) / (cmax - cmin)
    b = tmax - a * cmax
    T = a * gris.astype(float) + b

    rayon = np.arange(C) * x  # ring radius of each column
    U = np.sum(C_EAU * (T - tmin) * (2 * np.pi * rayon[np.newaxis, :]) * (x * y) * RHO_EAU)
    return float(U)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("image", help="thermal camera image (jpg/png)")
    parser.add_argument("--tmin", type=float, default=20, help="min of the colour scale (deg C)")
    parser.add_argument("--tmax", type=float, default=60, help="max of the colour scale (deg C)")
    parser.add_argument("--width", type=float, default=0.03, help="real width of the photo (m)")
    parser.add_argument("--height", type=float, default=0.1, help="real length of the photo (m)")
    args = parser.parse_args()

    img = Image.open(args.image).convert("RGB")
    U = variation_energie_interne(img, args.tmin, args.tmax, args.width, args.height)
    print("la variation d'énergie interne de l'ellipsoïde est de", U, "J")
