from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = []
if rank == 0:
    data = [*range(size)]
data = comm.scatter(data, root=0)


print(f"my rank is {rank}: {data}")
