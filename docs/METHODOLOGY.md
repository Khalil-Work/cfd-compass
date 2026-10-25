# How the directory is assembled

CFD Compass is a curated reference to software and resources created by their respective upstream teams. It is not a new solver, a distribution of their source code, or a scientific certification programme.

## Evidence recorded per entry

- Canonical `owner/repository`, official documentation and primary source links.
- An original summary, a concrete use case, cross-cutting tags and a material selection caveat where known.
- An editorial maturity label: **established**, **research** or **emerging**. These describe intended context, not a quality score.
- A dated GitHub API snapshot: default branch, main language, stars, archive/fork flags, licence identifier and last push time.

## What checking means

Descriptions were checked against project-owned repositories/documentation. Repository metadata was fetched from GitHub and redirects were resolved to canonical names. The validator checks structure, ownership consistency, duplicate repositories, source URLs and metadata coverage. That does not prove the linked software's numerical accuracy, security, current installability or suitability for a particular engineering decision. Those require problem-specific evaluation.

`pushed_at` is a repository activity timestamp; it is not a release date or a promise of support. **Archived** is an API flag. A project can be unmaintained without being archived, so explicit upstream notices are kept as caveats. **NOASSERTION** means automated licence classification is inconclusive; inspect the actual terms. Public visibility alone does not confer unrestricted reuse rights. Official GitHub mirrors are identified when development happens elsewhere.

## Inclusion and organization

The collection spans engineering CFD, specialist flow physics, numerical infrastructure, geometry/meshing, visualization, learning, benchmarks and workflows. A general scientific tool is included only when its role in a CFD workflow is clear. One canonical repository appears once, under its main purpose; tags cover overlap. Necessary official resources outside GitHub are listed separately rather than replaced by unofficial mirrors.

The collection favors documented utility and broad coverage. It does not claim to include every available code or rank projects by scientific accuracy. A popular project may be inactive; a small project may be valuable. Stars are shown only as dated metadata.

## Updating and correcting

The release PDF is a versioned snapshot. The README and searchable directory can evolve through reviewed changes. Automated link audits produce reports for maintainers; they do not silently endorse a moved URL or rewrite descriptions. The source JSON is the single catalogue source for README/category pages, CSV, website data and the PDF. Please report corrections with primary evidence.
