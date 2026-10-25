<a id="multiphase-spray"></a>

## 💧 Multiphase flow, droplets & sprays

Interfaces, dispersed phases, droplets and free-surface simulation.

| Project / use case | What it offers | Selection notes |
| --- | --- | --- |
| **[CFDEM coupling PUBLIC](https://github.com/CFDEMproject/CFDEMcoupling-PUBLIC)**<br>CFD-DEM particulate flow | Couples OpenFOAM flow calculations with discrete particle dynamics through selectable force and data-exchange models. Useful for studying fluidized beds, particulate transport and fluid-particle interaction workflows.<br>[Docs](https://github.com/CFDEMproject/CFDEMcoupling-PUBLIC#readme) · `GPL-3.0` | Established · Public and commercial product capabilities differ. Verify the documented OpenFOAM and particle-solver versions before installation. |
| **[JAX-Fluids](https://github.com/tumaer/JAXFLUIDS)**<br>Differentiable compressible multiphase research | Implements differentiable compressible flow simulation with high-order reconstruction, level-set and diffuse-interface two-phase methods. Enables research connecting numerical fluid dynamics, automatic differentiation and accelerator-based computation.<br>[Docs](https://jax-fluids.readthedocs.io/) · `NOASSERTION` | Research · Differentiating a discrete solver does not automatically yield reliable gradients through shocks or interface events; examine discretization and sensitivity assumptions. |
| **[Mantaflow](https://github.com/thunil/mantaflow)**<br>Liquid and smoke algorithm prototyping | Combines a fluid-simulation core with Python scene definitions and an extensible plugin system. Supports liquid, smoke and learning experiments aimed at graphics-oriented fluid algorithm research.<br>[Docs](https://github.com/thunil/mantaflow) · `NOASSERTION` | Research · Designed primarily for computer-graphics research; attractive visual output alone does not establish engineering accuracy. |
| **[MFC](https://github.com/MFlowCode/MFC)**<br>Shock-bubble interaction and compressible mixtures | Solves compressible multiphase flows with interface models, bubble dynamics, phase-change options and particle tracking. Useful for investigating shock-interface interaction and other strongly compressible multiphase phenomena.<br>[Docs](https://mflowcode.github.io/) · `MIT` | Established · Different mixture, interface and bubble models make different assumptions; select the model appropriate to the physical scale and regime. |
| **[SPlisHSPlasH](https://github.com/InteractiveComputerGraphics/SPlisHSPlasH)**<br>SPH incompressibility and coupled particle scenes | Implements several incompressible SPH pressure solvers alongside viscosity, surface tension and rigid or deformable body coupling. Particularly useful for comparing particle-fluid simulation methods and visual experiments.<br>[Docs](https://splishsplash.readthedocs.io/) · `MIT` | Established · Originates in physically based graphics research; engineering use needs independent dimensional, resolution and validation checks. |

[Back to topics ↑](https://github.com/Khalil-Work/cfd-compass#browse-by-topic)


Snapshot: 2026-10-25. [Full index](https://github.com/Khalil-Work/cfd-compass).
