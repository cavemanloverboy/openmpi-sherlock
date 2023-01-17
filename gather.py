from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

data = rank * rank
print(f"my rank is {rank}: {data}")
data = comm.gather(data, root=0)
if rank == 0:
    print(f"my rank is {rank} and I gathered: {data}")
else:
    assert data is None
