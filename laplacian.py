from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Problem Parameters
HEIGHT_PER_RANK = 10000
WIDTH_PER_RANK = 10000
CORNER_TEMP = 100

# This will be repeatedly used
BELOW = np.arange(HEIGHT_PER_RANK-1)-1
BELOW[0] = 0
TOTAL_CELLS = HEIGHT_PER_RANK * WIDTH_PER_RANK * size

if rank == 0:
    print(f"The grid contains {TOTAL_CELLS:,} cells. We are using {size} ranks")
    sys.stdout.flush()

# Algorithm Parameters
TOLERANCE = 2e-4
MAX_ITER = WIDTH_PER_RANK * size * 100

# Initialize this rank's grid
grid = np.zeros((WIDTH_PER_RANK, HEIGHT_PER_RANK))

# Initial conditions
if rank == 0:
    grid[0,:] = CORNER_TEMP * np.arange(HEIGHT_PER_RANK)/(HEIGHT_PER_RANK-1)
grid[:,-1] = CORNER_TEMP * np.arange((size-rank)*WIDTH_PER_RANK, (size-rank-1)*WIDTH_PER_RANK, -1)/(size*WIDTH_PER_RANK-1)


# Buffers
left_edge = np.empty(HEIGHT_PER_RANK-1, dtype=np.float64)
right_edge = np.empty(HEIGHT_PER_RANK-1, dtype=np.float64)


# Main loop
niter = 0
global_delta = np.array(np.inf)
while (global_delta > TOLERANCE) & (niter < MAX_ITER):

    # Increment iteration counter
    niter += 1

    # Send left edge to left rank if needed
    need_to_send_left_edge = rank > 0
    need_to_recv_left_edge = rank < size - 1
    if need_to_send_left_edge:

        # Get left edge
        left_edge_to_send = grid[0,:-1]

        # Send to left rank
        left_rank = rank - 1
        comm.Send(left_edge_to_send, dest=left_rank, tag=rank)
    if need_to_recv_left_edge:
        # Receive left edge from right rank
        right_rank = rank + 1
        comm.Recv(buf=left_edge, source=right_rank, tag=right_rank)

    # Send right edge to right rank if needed
    need_to_send_right_edge = rank < size - 1
    need_to_recv_right_edge = rank > 0
    if need_to_send_right_edge:

        # Get right edge
        right_edge_to_send = grid[-1,:-1]

        # Send to right rank
        right_rank = rank+1
        right_send = comm.Send(right_edge_to_send, dest=right_rank, tag=rank)
    if need_to_recv_right_edge:
        # Receive right edge from left rank
        left_rank = rank - 1
        comm.Recv(buf=right_edge, source=left_rank, tag=left_rank)


    # While we send left and right edge (if needed)
    # do work on center for which we have all neighbors
    right = grid[2:,:-1]
    left  = grid[:-2,:-1]
    above = grid[1:-1,1:]
    below = grid[1:-1, BELOW]
    newgrid = (left + right + above + below) / 4.0
    delta = np.abs(newgrid-grid[1:-1,:-1]).sum()
    grid[1:-1,:-1] = newgrid

    # Update rightmost column if needed
    if need_to_recv_left_edge:

        # Update rightmost column
        # left_edge of right rank is to our right
        right = left_edge
        left  = grid[-2,:-1]
        above = grid[-1,1:]
        below = grid[-1:,BELOW]
        newgrid = (left + right + above + below) / 4.0
        delta += np.abs(newgrid-grid[-1,:-1]).sum()
        grid[-1,:-1] = newgrid

    # Update leftmost column
    if need_to_recv_right_edge:

        # Update leftmost column
        # right_edge of left rank is to our left
        left = right_edge
        right  = grid[2,:-1]
        above = grid[0,1:]
        below = grid[0,BELOW]
        newgrid = (left + right + above + below) / 4.0
        delta += np.abs(newgrid-grid[0,:-1]).sum()
        grid[0,:-1] = newgrid


    # Now, we need a global synchronization...
    # Have we converged?
    # First, reset to zero
    global_delta = np.array(0.0)
    # Then, allreduce delta into global_delta
    comm.Allreduce(delta, global_delta, op=MPI.SUM)
    # Now, do a single division
    global_delta /= TOTAL_CELLS

    # Print for fun
    if rank == 0:
        print(f"global_delta({niter:06d}) = {global_delta:.2e}")
        sys.stdout.flush()


if rank == 0:
    if niter < MAX_ITER:
        print(f"Gauss-Seidel converged in {niter} steps. delta = {global_delta}")
    else:
        print(f"Gauss-Seidel did not converge in {MAX_ITER=} steps. delta = {global_delta}")
    print(f"The grid contained {TOTAL_CELLS:,} cells. We used {size} ranks")
    sys.stdout.flush()


np.save(f"row_avg_{rank:05}", grid.mean(0))
