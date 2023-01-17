from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

data = {}
if rank == 0:
    data = {'a': 7, 'b': 3.14}
data = comm.bcast(data, root=0)


print(f"my rank is {rank}: {data}")
