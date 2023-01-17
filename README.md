# OpenMPI on Sherlock

To get started with OpenMPI on Sherlock using conda,
```bash
conda create --name=openmpi python=3.11
conda activate openmpi
ml openmpi
pip install mpi4py
```
Note that Python 3.11 is not required (and that you can use an existing conda environment). But, 3.11 is O(40%) faster than 3.10 (by their own benchmarks), which is O(40%) faster than 3.9 due to recent efforts to make Python faster.

Once that is done, submit a SLURM job and use `srun python your_script.py` with it.

For an interactive job (e.g. for dev purposes) such as the one I used during my demo, fill out `N`, `T`, and `C`, `D-HH:MM:SS` here:
```
salloc -p kipac --nodes=N --tasks-per-node=T --cpus-per-task=C --time=D-HH:MM:SS bash
```
and then use `srun python your_script.py` to use the allocation.
