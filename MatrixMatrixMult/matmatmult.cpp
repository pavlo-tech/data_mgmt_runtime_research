#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctime>

#ifdef ZFP
#include "zfparray2.h"
#endif

#ifndef DATA_TYPE
#define DATA_TYPE double
#endif

// for now, we are only using square matrices
#ifndef MATRIX_WIDTH
#define MATRIX_WIDTH 1
#endif


// for now, we are only using square tiles
#ifndef TILE_SIZE
#define TILE_SIZE 1
#endif
#define TILE_M TILE_SIZE
#define TILE_N TILE_SIZE


#define NTIMES 5
#define A_VALUE 1
#define B_VALUE 2

template <typename T>
#ifdef ZFP
void print_matirx(zfp::array2<T> matrix, int m, int n)
#else
void print_matrix(T matrix[], int m, int n)
#endif
{
	int r,c;

 	for (r = 0; r < m; ++r)
	{
		printf("|\t");

		for (c = 0; c < n; ++c)
		{
			printf("%lf\t", (double)matrix[r*n + c]);
		}
		printf("|\n");
	}
}

template <typename T>
#ifdef ZFP
void init_mat_value(zfp::array2<T> A, int A_m, int A_n, T value)
#else
void init_mat_value(T A[], int A_m, int A_n, T value)
#endif
{
	int i,j; 
	for (i = 0; i < A_m; ++i)
		for (j = 0; j < A_n; ++j)
			A[i * A_n + j] = value;
}

template <typename T>
#ifdef ZFP
void multMat(zfp::array2<T> A, int A_m, int A_n, zfp::array2<T> B, int B_m, int B_n, zfp::array2<T> AB)
#else
void multMat(T A[], int A_m, int A_n, T B[], int B_m, int B_n, T AB[])
#endif
{
	/*A_n must = B_m*/

	int i,j,k;
	T sum;

	for (i = 0; i < A_m; ++i) // for each row of A
	{
		for (j = 0; j < B_n; ++j) // for each col of B
		{
			for (sum=0, k = 0; k < A_n; ++k) // sum across row of A and column of B
			{
				sum += (A[i * A_n + k] * B[k * B_n + j]);
			}
			AB[i * A_n + j] = sum;
		}
	}
}

template <typename T>
#ifdef ZFP
void multMat_tiled(zfp::array2<T> A, int A_m, int A_n, zfp::array2<T> B, int B_m, int B_n, zfp::array2<T> AB)
#else
void multMat_tiled(T A[], int A_m, int A_n, T B[], int B_m, int B_n, T AB[])
#endif
{
	/* AB must be memset to 0 */
	/* A_n must = B_m */
	/* A_m must be divisible by tile_m */
	/* B_n must be divisible by tile_n */

	int i,j,k,m,n;

	for (i = 0; i < A_m; i += TILE_M) // for each row of A
	{
		for (j = 0; j < B_n; j += TILE_N) // for each col of B
		{
			for (k = 0; k < A_n; ++k) // sum across row of A and column of B
			{
				for (m = 0; m < TILE_M; ++m) // sum for all values in tile
				{
					for (n = 0; n < TILE_N; ++n)
					{
						AB[(i + m) * A_n + (j + n)]  += (A[(i + m) * A_n + k] * B[k * B_n + (j + n)]);
					}
				}
			}
		}
	}
}


// declare variables
#ifdef ZFP
zfp::array2<DATA_TYPE> 
		A(MATRIX_WIDTH, MATRIX_WIDTH, RATE, 0, CSIZE),
		B(MATRIX_WIDTH, MATRIX_WIDTH, RATE, 0, CSIZE),
		AB(MATRIX_WIDTH, MATRIX_WIDTH, RATE, 0, CSIZE);
#else
DATA_TYPE 
		A[MATRIX_WIDTH * MATRIX_WIDTH],
		B[MATRIX_WIDTH * MATRIX_WIDTH],
		AB[MATRIX_WIDTH * MATRIX_WIDTH];
#endif

int main()
{
	// initialize values
	init_mat_value(A, MATRIX_WIDTH, MATRIX_WIDTH, (DATA_TYPE)A_VALUE);
	init_mat_value(B, MATRIX_WIDTH, MATRIX_WIDTH, (DATA_TYPE)B_VALUE);


	for (int i = 0; i < NTIMES; ++i)
	{
		// clear AB
		init_mat_value(AB, MATRIX_WIDTH, MATRIX_WIDTH, (DATA_TYPE)0);

		printf("%d,",i);

		clock_t begin = clock();
		#ifdef TILED
		multMat_tiled(A, MATRIX_WIDTH, MATRIX_WIDTH, B, MATRIX_WIDTH, MATRIX_WIDTH, AB);
		#else
		multMat(A, MATRIX_WIDTH, MATRIX_WIDTH, B, MATRIX_WIDTH, MATRIX_WIDTH, AB);
		#endif
		clock_t end = clock();
		double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;

		printf("%lf\n", elapsed_secs);
	}
}




