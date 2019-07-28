#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <signal.h>
//#include <mpi.h>

#include "util.h"
#include "init.h"
//#include "include/Instrumentation.h"
//#include "src/corrupt/corrupt.h"



int main(int argc, char** argv)
{
    csr_matrix* A;
    double* x0, *xstar, *b0, *bstar;
    int i = 0;
    printf("start\n");
    if (argc < 2) {
        printf("Error Usage: ./AMG.out /path/to/matrix.mtx\n");
        exit(argc);
    }
   
    
    printf("\n\n\n            Initializing Matrix\n---------------------------------------------------\n");
    printf("Read matrix file:    %s\n", argv[1]);
    
    A = (csr_matrix*) malloc(sizeof(csr_matrix));
    /* read A */
    readMM(argv[1], A);
    printf("Read matrix: M = %d, N = %d, NNZ = %d\n", A->m, A->n, A->nnz);
    
    x0 = (double*) malloc(sizeof(double) * A->n);
    xstar = (double*) malloc(sizeof(double)*A->n);
    for(i = 0; i < A->n; i++) {
        x0[i] = 1.0;
        xstar[i] = 1.0;
    }
    b0 = calloc(A->n, sizeof(double));
    bstar = calloc(A->n, sizeof(double));

    printf("SPMV**********\n");
    /* setting b0 based on xstar */
    int nIter = 1;
    //copyMem2Faulty(-1);
    for (i = 0; i < nIter; i++) {
        csr_matvec(A, x0, b0);
        //jacobi(A, x0, bstar, b0, 2./3., 0, A->n, 1);
        double d;
        dot(b0, b0, A->n, &d);
        d = sqrt(d);
        printf("Norm: %g\n",d);
        double* tmp = x0; x0 = b0; b0 = tmp;
        //   for (j=0; j< A->n; j++)
       //     x0[j] = b0[j];
            //x0[j] = b0[j]/d;
    }
    //csr_matvec(A, xstar, b0);

/*** for jacobi
    double max = 0;
    for(i = 0; i < A->n; i++) {
        double diff = fabs(b0[i] - bstar[i]);
        if (diff > max)
            max = diff;
    }
    printf("Inf Norm: %g\n", max); 
*/


    free(A->I);
    free(A->J);
    free(A->V);
    free(A);
    free(x0);
    free(xstar);
    free(bstar);
    free(b0);
    printf("return 0;\n");
    return 0;
}


