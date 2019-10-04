#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <signal.h>
//#include <mpi.h>
#include <iostream>
#include <ctime>
#include "util.h"
#include "init.h"
//#include "include/Instrumentation.h"
//#include "src/corrupt/corrupt.h"



int main(int argc, char** argv)
{
    csr_matrix* A;

		double *xstar, *bstar;
    int i = 0;
    //printf("start\n");
    if (argc < 2) {
        printf("Error Usage: ./AMG.out /path/to/matrix.mtx\n");
        exit(argc);
    }
   
    
    //printf("\n\n\n            Initializing Matrix\n---------------------------------------------------\n");
    //printf("Read matrix file:    %s\n", argv[1]);
    
    A = (csr_matrix*) malloc(sizeof(csr_matrix));
    /* read A */
    readMM(argv[1], A);
    //printf("Read matrix: M = %d, N = %d, NNZ = %d\n", A->m, A->n, A->nnz);

#ifdef ZFP
		zfp::array1<double>
			x0(A->n, RATE, 0, CSIZE), 
			b0(A->n, RATE, 0, CSIZE);
#else    
    double *x0 = (double*) malloc(sizeof(double) * A->n);
		double *b0 = (double*)calloc(A->n, sizeof(double));
#endif

    xstar = (double*) malloc(sizeof(double)*A->n);
    for(i = 0; i < A->n; i++) {
        x0[i] = 1.0;
        xstar[i] = 1.0;
    }
    bstar = (double*)calloc(A->n, sizeof(double));

    //printf("SPMV**********\n");
    /* setting b0 based on xstar */
    int nIter = 5;
    //copyMem2Faulty(-1);
		 printf("Iteration,Time,Norm\n");
    for (i = 0; i < nIter; i++) 
		{
			 	clock_t begin = clock();
        csr_matvec(A, x0, b0);
				clock_t end = clock();
    		double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

        double d;
        d = sqrt(d);
				printf("%d,%lf,%lf\n", i, elapsed_secs, d);
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

		//std::cout<<"\nb0:"<< std::endl;
		//for(int i = 0; i < A->n; ++i) std::cout << b0[i] << std::endl;
    free(A->I);
    free(A->J);
#ifdef ZFP
		delete A->V;
		//printf("\nDELETED!\n");
#else
    free(A->V);
    free(x0);
    free(b0);
#endif
    free(A);
    free(xstar);
    free(bstar);
    //printf("return 0;\n");
    return 0;
}


