#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/time.h>
#include <assert.h>
/*#include <vecLib/cblas.h> */
/*#include <vecLib/clapack.h> */
#include "util.h"

/*
        Input:
                hierarchy:
                nu1:            number of pre-smooth iterations
                nu2:            number of post-smooth iterations
                relax:          intialized relaxation method to use
                nlevels:        number of levels to use in the hierarchy 
                x0:                     initial guess to solution
                b:                      RHS of linear system (MUST be pre-allocated)
                tol:            tolerance 

        Output:
                residuals       array of the residual vector for each level

*/

double* solve(ml hierarchy, int nu1, int nu2, int nlevels, double x0[], 
                                double b0[], double tol, int maxiter)
{
    int i, j, ITER;
    const double omega = 2.0/3.0;
    csr_matrix* A = hierarchy.levels[0].A;

    double* residuals = (double*) calloc(maxiter, sizeof(double));
    double* x_copy    = (double*) malloc(A->n * sizeof(double));
    double* A_dense   = (double*) malloc(hierarchy.levels[nlevels-1].A->m*hierarchy.levels[nlevels-1].A->n*sizeof(double));
    int* ipiv         = (int*) malloc(sizeof(int)*hierarchy.levels[nlevels-1].A->n);
    double* Ax        = (double*) malloc(sizeof(double) * A->n);
    double* temp      = (double*) malloc(sizeof(double) * A->n);

    for (i=0; i<A->n; i++) {
        hierarchy.levels[0].x[i] = x0[i];
        hierarchy.levels[0].b[i] = b0[i];
    }
    assert(nu1 % 2 == 0 && "nu1 must be even");
    assert(nu2 % 2 == 0 && "nu2 must be even");
    printf("Solving %d x %d prolem with %d levels to a tolerance of %g\n\n", A->n, A->m, nlevels, tol);
    residual_norm(A, hierarchy.levels[0].x, hierarchy.levels[0].b, Ax, &residuals[0]);
    ITER = 0;

    while(ITER < maxiter && residuals[ITER] > tol) {
        ITER++;
        /*
         for (j = 0; j < A->n; j++)
            x_copy[j] = hierarchy.levels[0].x[j];
        */

        /* traverse down */
        for(i =0; i < nlevels-1; i++) {
            /* smooth x */
            A = hierarchy.levels[i].A;
            for (j=0; j < nu1; j++) {
                jacobi(A, hierarchy.levels[i].x, hierarchy.levels[i].b, x_copy, omega, 0, A->m, 1);
                swapD_ptr(&hierarchy.levels[i].x, &x_copy);
                /* Not efficient but currently swaping  pointers causes the fault injector segfault */
                /*
                 * if(nu1 % 2 == 1) {
                    if (j % 2 == 0)
                        jacobi(A, x_copy, hierarchy.levels[i].b, hierarchy.levels[i].x, omega, 0, A->m, 1);
                    else
                        jacobi(A, hierarchy.levels[i].x, hierarchy.levels[i].b, x_copy, omega, 0, A->m, 1);
                }
                else {
                    if (j % 2 == 0)
                        jacobi(A, hierarchy.levels[i].x, hierarchy.levels[i].b, x_copy, omega, 0, A->m, 1);
                    else
                        jacobi(A, x_copy, hierarchy.levels[i].b, hierarchy.levels[i].x, omega, 0, A->m, 1);
                }
                */
            }

            /* restrict residual */
            residual(A, hierarchy.levels[i].x, hierarchy.levels[i].b, Ax, temp);
            csr_matvec(hierarchy.levels[i].R, temp, hierarchy.levels[i+1].b);

            /* populate x */
            for (j = 0; j < hierarchy.levels[i+1].A->m; j++) {
                hierarchy.levels[i+1].x[j] = 0.0;
                //x_copy[j] = 0.0;
            }
        }


        /* convert A from csr to dense */
        A = hierarchy.levels[nlevels-1].A;
        for(i=0; i< A->n * A->m; i++)
            A_dense[i] = 0.0;
        for(i = 0; i < A->n; i++) {
            for(j = A->I[i]; j < A->I[i+1]; j++) {
                int col_ind = A->J[j];
                A_dense[i + A->n*col_ind] = A->V[j];    /*column major*/
            }
        }

        /* coarse-grid solve */
        int nrhs = 1, n = A->n, lda = A->n, ldb = A->n, info;
        dgesv_(&n, &nrhs, A_dense, &lda, ipiv, hierarchy.levels[nlevels-1].b, &ldb, &info);
        for (j = 0; j < A->n; j++)
            hierarchy.levels[nlevels-1].x[j] = hierarchy.levels[nlevels-1].b[j];

        /* traverse up */
        for(i = nlevels-2; i >= 0; i--) {
            A = hierarchy.levels[i].A;
            int length = hierarchy.levels[i].P->n;

            /* prolongate x */
            csr_matvec(hierarchy.levels[i].P, hierarchy.levels[i+1].x, Ax);

            /* correct x */
            for(j = 0; j < length; j++) {
                hierarchy.levels[i].x[j] = hierarchy.levels[i].x[j] + Ax[j];
                //x_copy[j] = hierarchy.levels[i].x[j];
            }

            /* post smooth */
            for(j = 0; j < nu2; j++) {
                jacobi(A, hierarchy.levels[i].x, hierarchy.levels[i].b, x_copy, omega, 0, A->m, 1);
                swapD_ptr(&hierarchy.levels[i].x, &x_copy);
                /* Not efficient but currently swaping  pointers causes the fault injector segfault */
                /*
                 * if(nu1 % 2 == 1) {
                    if (j % 2 == 0)
                        jacobi(A, x_copy, hierarchy.levels[i].b, hierarchy.levels[i].x, omega, 0, A->m, 1);
                    else 
                        jacobi(A, hierarchy.levels[i].x, hierarchy.levels[i].b, x_copy, omega, 0, A->m, 1);
                }
                else {
                    if (j % 2 == 0)
                        jacobi(A, hierarchy.levels[i].x, hierarchy.levels[i].b, x_copy, omega, 0, A->m, 1);
                    else
                        jacobi(A, x_copy, hierarchy.levels[i].b, hierarchy.levels[i].x, omega, 0, A->m, 1);
                }
                */
            }
        }
        residual_norm(hierarchy.levels[0].A, hierarchy.levels[0].x, hierarchy.levels[0].b, Ax, &residuals[ITER]);
    }
    free(x_copy);
    free(A_dense);
    free(ipiv);
    free(Ax);
    free(temp);

    return residuals;
}

