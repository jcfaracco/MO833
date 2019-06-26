# GROMACS and OPM samples generator and instrumentation
-----------------------

This is a project related to test automation and instrumentation of GROMACS and OPM only.

It was created to generate samples to measure performance between multiple machine configurations.

Specially GROMACS which supports OpenMP, MPI and GPUs.

The intention of the Ansible scripts developed by this project is help users to generate samples and run their benchmarks to measure system performance.

### Project Structure
-----------------------

This project is a collection of scripts: Ansible, Docker, Singularity, Python and even Shell Script.

- Ansible scripts (`scripts/ansible`): All scripts related to machine provisioning. Tests require machine with pre-installed software. This collection allocate machines at Amazon EC2 and installs all dependencies into target machines.
- Docker scripts (`scripts/docker`): An agent to start tests is required. So, to avoid incompatible problems with libraries, tools and versioning, this container isolate this jail from your clean and healty OS.
- Python scripts (`scripts/python`): Generate the CSV reports after executing testcases.
- Shell scripts (`./*`): Join everything metioned above.

Where are singularity scripts then? It is not part of the process building containers, but you can find them insto `scripts/ansible/tasks/{opm,gromacs}/singularity`. They help anyone to generate you own image and reproduce our tests. Or, if you would like to have fun. ;-)

### Basic Usage
-----------------------

As mentioned above, this project only generate samples based on GROMACS or OPM. The process is divided into 4 items:

Generate your target machines with `setup` script (requires: your PEM key, test case and Amazon credentials):

    $ ./setup -k /foo/bar/my-scret.pem -c /biz/baz/credentials -t opm

*Important:* Do not rename your PEM key. It is used to assign the correct key name into Amazon EC2.
