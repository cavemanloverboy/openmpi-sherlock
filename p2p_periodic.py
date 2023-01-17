from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

comm.send(rank, dest=(rank+1)%size, tag=0)
data = comm.recv(source=(rank-1)%size, tag=0)

print(f"my rank is {rank}: {data}")
