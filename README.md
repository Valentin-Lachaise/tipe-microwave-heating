# Microwave heating: characterization and optimization

TIPE 2024/2025 (PC*), file N°35483.

Study of how microwaves heat a material and why hot spots appear, combining modelling, simulation and experiments.

Slides, in French: [tipe-microwave-heating-slides.pdf](docs/tipe-microwave-heating-slides.pdf)

## Motivation
In Courty's well-known experiment, a potato heated in a microwave oven shows hot spots that a thermal camera reveals. The goal is to understand where they come from and how to control them.

![Thermal image of the experiment we reproduced: cold zone, hot zone and temperature scale](docs/images/01_motivation_camera_thermique.png)

## Approach
- **Physics**: Mie resonances inside the heated object, evanescent waves, energy balance of the heating process.
- **Modelling**: Maxwell equations solved numerically in Python.
- **Experiments**: temperature mapping with a thermal camera, on agar-agar samples cast in 3D-printed waveguide moulds modelled in SolidWorks.
- **Application**: use of microwave heating for ester synthesis.

The slides are in French, so the captions of the images below are too.

## 1. Invalidating the "foci" theory
The hot spots are sometimes explained by the foci of an elliptical sample. For an ellipse, the ratio between the distance between the foci and the major axis is sqrt(1 - (b/a)²). Measured hot spot positions do not follow this prediction.

| Ellipse and its foci | Theory vs. experiment |
|---|---|
| ![Ellipse, foci and axes](docs/images/02_theorie_foyers_ellipse.png) | ![Invalidation of the foci theory](docs/images/03_invalidation_theorie_foyers.png) |

## 2. Reproducible waveguides
Agar-agar (20 g/L) has physical properties close to those of water. It is cast in 3D-printed shells modelled in SolidWorks, which gives reproducible samples that keep their spherical shape.

| Mould modelling | 3D printing of the shells | Agar-agar waveguide |
|---|---|---|
| ![Moulds modelled in SolidWorks](docs/images/04_modelisation_moules_solidworks.png) | ![3D printed shells](docs/images/05_impression_3d_coques.png) | ![Agar-agar cast in the mould](docs/images/06_guide_ondes_agar_agar.png) |

## 3. Analytical solutions
The wave equation in cylindrical coordinates has a solution that can be expanded as a power series (truncated at order 10) satisfying the boundary condition. The matrix equation is solved in Python. The computed electric field (left) is compared with the temperature profile measured in our experiment.

![Electric field found by our code and measured temperature profile](docs/images/07_solution_analytique_champ_electrique.png)

## 4. Experimental validation of the analytical models
The temperature profile along a section of the sample is compared with the square of Bessel functions (see [`src/bessel_squared.py`](src/bessel_squared.py) and [`src/temperature_profile.py`](src/temperature_profile.py)).

| Spheres | Thick cylinder | Thin cylinder |
|---|---|---|
| ![Validation for spheres](docs/images/08_validation_spheres.png) | ![Validation for a thick cylinder](docs/images/09_validation_cylindre_epais.png) | ![Validation for a thin cylinder](docs/images/10_validation_cylindre_fin.png) |

## 5. Energy study
The internal energy variation of the sample is computed from the thermal image ([`src/internal_energy.py`](src/internal_energy.py)). There is a shape that gives an optimal heating for a given volume.

![Energy results for each shape](docs/images/11_etude_energetique.png)

## 6. Application to a microwave chemical synthesis
Fischer esterification of ethanoic acid with 3-methylbutan-1-ol, heated for 1 minute at 570 W in the microwave oven. The remaining acid is titrated with sodium hydroxide.

| Protocol | Setup | Results |
|---|---|---|
| ![Esterification protocol and titration](docs/images/12_protocole_esterification.png) | ![Reagents in a glass ball inside the waveguide](docs/images/13_dispositif_synthese.png) | ![Thermal images and yields](docs/images/14_resultats_synthese.png) |

Heating and yield are optimal when the reagents are placed at the centre of the waveguide (75 % yield, against 49 % at the edge and 60 % without waveguide).

## Code

| File | Content |
|---|---|
| [`src/bessel_squared.py`](src/bessel_squared.py) | Plot of the squared Bessel functions J_n(kr)² |
| [`src/temperature_profile.py`](src/temperature_profile.py) | Thermal image → temperature as a function of radius along a section |
| [`src/internal_energy.py`](src/internal_energy.py) | Thermal image → internal energy variation of the sample |
| [`waveguide_cutoff.py`](waveguide_cutoff.py) | Cutoff frequencies of a rectangular waveguide |

```bash
pip install -r requirements.txt
python src/bessel_squared.py
python src/temperature_profile.py image.jpg --tmin 19.8 --tmax 49.8 --width 10 --height 5
python src/internal_energy.py image.jpg --tmin 20 --tmax 60 --width 0.03 --height 0.1
```

## Author
Valentin Lachaise, engineering student at IMT Atlantique.
Personal website: https://vlachaise.pages.dev
