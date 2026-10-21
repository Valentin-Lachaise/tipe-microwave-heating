"""Temperature profile along a section of a heated sample (thermal camera image).

The thermal camera image is converted to grey levels, then to temperatures
with an affine law T = a * grey + b such that the darkest grey level of the
image corresponds to Tmin and the brightest to Tmax (the two values read on
the camera colour scale). The profile is taken along the central column of the
image, from the bottom of the picture upwards.

Annex of the TIPE slides (slide 27): "code to plot the point curves (section
of the shape)". The pixel loops of the original script are vectorised with
numpy; the algorithm is unchanged.

Usage:
    python temperature_profile.py image.jpg --tmin 19.8 --tmax 49.8 \
        --width 10 --height 5 --title "section cylindre"
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def liste(image, tmin, tmax, larg, long):
    """Return the list of (temperature in deg C, radius in cm) tuples.

    image      : PIL image of the thermal camera picture
    tmin, tmax : temperatures (deg C) at the bottom/top of the colour scale
    larg, long : real width and length of the photo, in cm
    """
    matimage = np.array(image)
    L, C = matimage.shape[0], matimage.shape[1]
    y = long / L  # real length of one pixel (cm)

    # grey level = mean of the first two colour channels (as in the original)
    gris = (matimage[:, :, 0].astype(float) / 2 + matimage[:, :, 1].astype(float) / 2).astype(
        np.uint8
    )
    cmin, cmax = int(gris.min()), int(gris.max())
    if cmax == cmin:
        raise ValueError("The image is uniform: cannot calibrate the temperature scale.")

    a = (tmax - tmin) / (cmax - cmin)
    b = tmax - a * cmax

    # central column, read from the bottom of the image upwards
    colonne = gris[::-1, C // 2].astype(float)
    temperatures = a * colonne + b
    return [(float(t), i * y) for i, t in enumerate(temperatures)]


def tracer_points(l, titre="section"):
    """Plot temperature as a function of radius from a list of (T, r) tuples."""
    Y = [el[0] for el in l]
    X = [el[1] for el in l]
    plt.figure()
    plt.plot(X, Y, "rx")
    plt.xlabel("rayon (cm)")
    plt.ylabel("T (°C)")
    plt.title(f"Graphique de la température en fonction du rayon ({titre})")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("image", help="thermal camera image (jpg/png)")
    parser.add_argument("--tmin", type=float, default=19.8, help="min of the colour scale (deg C)")
    parser.add_argument("--tmax", type=float, default=49.8, help="max of the colour scale (deg C)")
    parser.add_argument("--width", type=float, default=10, help="real width of the photo (cm)")
    parser.add_argument("--height", type=float, default=5, help="real length of the photo (cm)")
    parser.add_argument("--title", default="section", help="shape name used in the plot title")
    args = parser.parse_args()

    img = Image.open(args.image).convert("RGB")
    points = liste(img, args.tmin, args.tmax, args.width, args.height)
    tracer_points(points, args.title)
