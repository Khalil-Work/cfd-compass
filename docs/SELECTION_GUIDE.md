# Choose a CFD stack by the problem

Start with the physical model and evidence you need, then choose software. Popularity is a discovery signal, not an accuracy measure.

## A practical decision sequence

1. **State the regime.** Compressible or incompressible? Laminar, transitional or turbulent? Steady or unsteady? Specify Mach/Reynolds ranges, dominant scales and required outputs.
2. **List the coupled physics.** Reacting chemistry, heat transfer, phase change, dispersed droplets, moving solids, radiation or porous transport can determine the solver family.
3. **Choose a discretization that fits.** Geometry and boundary layers often favor body-fitted meshes; high-order methods suit some accuracy-sensitive workloads; immersed boundaries and Cartesian adaptation have different geometry and conservation trade-offs. LBM and SPH solve different formulations and require their own resolution and boundary-condition checks.
4. **Check the complete workflow.** Geometry cleanup, meshing, boundary conditions, linear solvers, restart files, monitoring, data I/O and visualization matter as much as the time integrator.
5. **Budget the calculation.** Compare memory per cell, physical time steps, chemistry cost, output volume, available accelerators and the actual support matrix. A GPU label does not guarantee your case fits or runs faster.
6. **Plan verification and validation.** Use analytical solutions or manufactured solutions where suitable, mesh/time refinement, conservation checks, solver tolerances, benchmark comparisons and experimental uncertainty. Distinguish code verification from validation of a physical model.
7. **Check adoption constraints.** Read the upstream licence and documentation for your intended use, contribution location, install process, compatibility and maintenance signals.

## Suggested routes through the index

| Goal | Explore first | Confirm before committing time |
| --- | --- | --- |
| Learn the numerical foundations | Verification & learning, then general solvers | Units, boundary conditions, stability and grid convergence |
| External aerodynamics or design | General solvers, high-order methods, automation & UQ | Compressibility range, turbulence model, adjoint consistency |
| Flames, ignition or combustors | Reacting flows, then multiphase & sprays | Mechanism validity, stiffness, energy coupling and transport |
| Droplets, sprays or free surfaces | Multiphase & sprays, kinetic & particle methods | Interface treatment, phase-change assumptions and mass conservation |
| Wall-bounded turbulence | Turbulence & HPC, high-order methods | Near-wall resolution, statistics duration and boundary forcing |
| Ocean, weather or wind energy | Environmental flows | Earth-system forcing, closure assumptions, grids and nesting |
| Fluid-structure or biomedical flow | Coupled & specialist tools | Interface conservation, coupling stability and constitutive models |
| Inverse design or surrogate models | Scientific ML & ROM, automation & UQ | Training/test separation, out-of-distribution behavior and gradient checks |

## A compact reproducibility record

Save the upstream version/commit, mesh, physical parameters and units, initial/boundary conditions, model choices, solver tolerances, time step/CFL, hardware and precision, command/environment, post-processing script, comparison data and uncertainty. Keep enough information for another person to reproduce a quantity of interest, not just a screenshot.

## Emerging methods

Differentiable solvers, neural operators and GPU-native frameworks are valuable research directions. Check whether your required physics, boundary conditions, precision, geometry and gradients are actually supported. An automatic-differentiation gradient can still depend on the discrete solver, stopping criteria and treatment of discontinuities. Compare learned models to a suitable numerical baseline and preserve an independent test set.
