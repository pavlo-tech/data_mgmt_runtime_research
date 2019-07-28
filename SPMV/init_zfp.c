#include <stdlib.h>
#include <stdio.h>
void INIT(int argc, char** argv)
{
    /*
 *  int argc=1;
    const char* argv[2];
    const char* prgm = "./SpMV.out";
    argv[0] = prgm;
    argv[1] = 0;
    */

    printf("MPI_INIT\n");
    return MPI_Init(&argc, &argv);
}

