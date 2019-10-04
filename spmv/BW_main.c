#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <signal.h>
//#include <mpi.h>

#include "util.h"
#include "include/Instrumentation.h"
#include "src/corrupt/corrupt.h"
int CYCLE = 123;

double countDown()
{
    return CYCLE--;
}

void sigHandler(int sig)
{
    printf("Receiving Sig %d\n", sig);
    printStats();
    //dumpMemory(0,-1,"gold.txt", "faulty.txt");
    fflush(stdout);
    exit(sig);
}

int main(int argc, char** argv)
{
    MPI_Init(&argc, &argv);
    csr_matrix* A;
    double* x0, *xstar, *b0, *bstar;
    int N = 1, i = 0;
    char path [1000];
    FILE* f;

    if (argc < 2) {
        printf("Error Usage: ./AMG.out /path/to/matrices\n");
        exit(argc);
    }
   
    if (signal (SIGSEGV, sigHandler) == SIG_ERR)
        printf("Error setting segfault handler...\n");
    if (signal (SIGBUS, sigHandler) == SIG_ERR)
        printf("Error setting bus error handler...\n");
    
    CYCLE = atoi(argv[argc-1]); 
    printf("Init FlipIt\n");
    FLIPIT_Init(0, argc, argv, atol(argv[argc-1]));
    FLIPIT_SetInjector(0);
    FLIPIT_SetFaultProbability(countDown);
    printf("\n\n\n            Initializing Matrix\n---------------------------------------------------\n");
    strcpy(path, argv[1]);
    int len = strlen(path);
    strcat(path, "/info.txt");

    printf("Reading Directory:    %s\n", argv[1]);
    if ((f = fopen(path, "r")) == NULL) 
        return -1;
    //fclose(f);

    printf("*********\n");
    A = (csr_matrix*) malloc(sizeof(csr_matrix));
    /* read A */
    strcpy(path+len, "/A");
    sprintf(path + len + 2, "%d", N);
    strcat(path, ".mtx");
    printf("readMM*****\n");
    readMM(path, A);
    printf("Read matrix file:    %s\n", path);
    
    x0 = (double*) malloc(sizeof(double) * A->n);
    xstar = (double*) malloc(sizeof(double)*A->n);
    for(i = 0; i < A->n; i++) {
        x0[i] = 1.0;
        xstar[i] = 1.0;
    }
    b0 = calloc(A->n, sizeof(double));
    bstar = calloc(A->n, sizeof(double));

    /* setting b0 based on xstar */
    FLIPIT_SetInjector(1);
    int nIter = 5;
    //copyMem2Faulty(-1);
    for (i = 0; i < nIter; i++) {
        csr_matvec(A, x0, b0);
        //jacobi(A, x0, bstar, b0, 2./3., 0, A->n, 1);
        double d;
        dot(b0, b0, A->n, &d);
        d = sqrt(d);
        printf("Norm: %g\n",d);
        printStats();    
       // dumpMemory(0,-1,"gold.txt", "faulty.txt");
        printf("x=%p\tb=%p\n", x0, b0);
        double* tmp = x0; x0 = b0; b0 = tmp;
        printf("x=%p\tb=%p\n", x0, b0);
        //   for (j=0; j< A->n; j++)
       //     x0[j] = b0[j];
            //x0[j] = b0[j]/d;
    }
    FLIPIT_SetInjector(0);
    
    /* Stats */
   // printStats();    
    //csr_matvec(A, xstar, b0);
    
    double max = 0;
    for(i = 0; i < A->n; i++) {
        double diff = fabs(b0[i] - bstar[i]);
        if (diff > max)
            max = diff;
    }
    printf("Inf Norm: %g\n", max); 
    //printf("CYCLE = %d\n", CYCLE);
    

    //FLIPIT_Finalize("HISTO.txt");
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


