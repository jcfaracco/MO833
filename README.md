# GROMACS and OPM samples generator and instrumentation
-----------------------

This is a project related to test automation and instrumentation of GROMACS and OPM only.

It was created to generate samples to measure software performance across multiple machine configurations. Specially GROMACS which supports OpenMP, MPI and GPUs.

The intention of these Ansible scripts developed by this project is help users to generate samples and run their benchmarks to measure system performance.


### Project Structure
-----------------------

This project is a collection of scripts: Ansible, Docker, Singularity, Python and even Shell Script.

- Ansible scripts (`scripts/ansible`): All scripts related to machine provisioning. Tests require machine with pre-installed software. This collection allocate machines at Amazon EC2 and installs all dependencies into target machines.
- Docker scripts (`scripts/docker`): An agent to start tests is required. So, to avoid incompatible problems with libraries, tools and versioning, this container isolate this jail from your clean and healty OS.
- Python scripts (`scripts/python`): Generate the CSV reports after executing testcases.
- Shell scripts (`./*`): Join everything metioned above.
- Other directories (`data`): Contains collected data from test case(s) like charts, profiling and others.
- Other directories (`templates`): Contains templates to plot data from CSV files.

Where are singularity scripts then? It is not part of the process building containers, but you can find them insto `scripts/ansible/tasks/{opm,gromacs}/singularity`. They help anyone to generate you own image and reproduce our tests. Or, if you would like to have fun. ;-)


### Basic Usage
-----------------------

As mentioned above, this project only generate samples based on GROMACS or OPM. The process is divided into 4 items:

1.Generate your target machines with `setup` script (requires: `-k` your PEM key, `-t` test case `{opm,gromacs}` and `-c` Amazon credentials):

    $ ./setup -k /foo/bar/my-scret.pem -c /biz/baz/credentials -t opm

**Important:** Do not rename your PEM key. It is used to assign the correct key name into Amazon EC2.

2.Run your test cases passing a target machine (requires `-t` test case `{opm,gromacs}`, `-m` machine target, `-s` test case size `{large,small}`):

    $ ./test -k /foo/bar/my-scret.pem -t gromacs -m p2.xlarge -s small -p 8 -l 10

Other arguments are optional: `-p` for OpenMP number of processes and `-l` for loops (or number of samples).

3.Generate report data (CVS file) from output (requires only `-t` test case `{opm,gromacs}`):

    $ ./report -d /foo/bar/output/ -t opm
    
Only directory `-d` is an optional argument because the script automatically considers the `output/` directory generated at the current directory.

From here, you can check the `results.csv` file and use it according one of templates inside `templates/` directory.

4.To clean up the allocated machines after performing your test cases, you can execute the last script provided:

    $ ./cleanup -k /foo/bar/my-scret.pem
    
This part will terminate all instances allocated for this test process.


### Authors
-----------------------
Julio Faracco
Rodrigo Bartolomeu
