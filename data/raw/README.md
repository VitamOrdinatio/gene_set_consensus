# data/raw

This directory is reserved for tiny demonstration inputs only.

Do not store real MitoCarta, GTR, Epi25, or other large source files here.

Real source files should live outside Git:

- sys76: `/mnt/storage/gene_sets/`
- sys76 GTR: `/mnt/storage/gtr/`
- MARK: `/data/storage/gene_sets/`
- MARK GTR: `/data/storage/gtr/`

Phenotype config files point to those external locations using `file_path`.
