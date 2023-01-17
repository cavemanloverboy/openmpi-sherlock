from mpi4py import MPI
from time import perf_counter as time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

PINGS = 200

if rank == 0:
    start = time()

    counter = 0
    send_counter = 0
    while send_counter < PINGS:

       counter += 1
       comm.send(counter, dest=1, tag=11)
       counter = comm.recv(source=1, tag=11)

       send_counter += 1

    ping_time = time()-start
    print(f"pinged back and forth {PINGS} times in {ping_time:.8f} seconds")

    start = time()
    counter = 0
    for _ in range(2*PINGS):
        counter += 1
    increment_time = time()-start
    print(f"incremented counter in {PINGS} times in {increment_time:.8f} seconds, {ping_time/increment_time:.2f} factor difference")

elif rank == 1:
    reply_counter = 0
    while reply_counter < PINGS:

       counter = comm.recv(source=0, tag=11)
       counter += 1
       comm.send(counter, dest=0, tag=11)

       reply_counter += 1

else:
    print(f"I am rank {rank} and I'm sitting this one out, boss")
