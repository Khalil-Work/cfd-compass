# Security and safe use

This repository contains a catalogue, static website and build tools. It does not download or execute the listed projects. Review upstream install instructions, licences, dependencies and integrity checks before running third-party software.

For a security problem in CFD Compass itself, use [private vulnerability reporting](https://github.com/Khalil-Work/cfd-compass/security/advisories/new). For a vulnerability in a listed project, follow that project's security policy instead. Do not include credentials, unpublished data or exploit payloads in public catalogue issues.

Only the current default branch of this directory is maintained. Static content is untrusted input to the renderer: HTML is escaped, repository IDs and URLs are validated, and CI does not execute catalogue-linked code. Pull-request checks run with read-only permissions; scheduled audits do not post public comments or auto-merge changes.
