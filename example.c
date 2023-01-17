#include <iostream>
#include <mpi.h>
#include <unistd.h>

int main(int argc, char* argv[])
{
    MPI_Init(&argc, &argv);
    MPI_Request request;
    MPI_Status  status;

    int size, rank, data;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank>0) {
       MPI_Irecv(&data, 1, MPI_INT, rank - 1, 0,  MPI_COMM_WORLD,&request);
       MPI_Wait(&request, &status);
       std::cout << "Rank " << rank << " has received message with data " << data<< " from rank " << rank - 1
              << std::endl;
    }

    std::cout << "Hello from rank " <<rank << " out of " << size<< std::endl;
    data=rank;

   if(rank + 1 < size){
       MPI_Isend(&data, 1, MPI_INT, (rank + 1), 0, MPI_COMM_WORLD, &request);
    }
    MPI_Wait(&request, &status);
    MPI_Finalize();

    return 0;
}
