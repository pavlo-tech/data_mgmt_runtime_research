#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctime>
#include <math.h>

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

#ifdef ZFP
void print_matrix(zfp::array2<DATA_TYPE> matrix, int m, int n)
#else
void print_matrix(DATA_TYPE matrix[], int m, int n)
#endif
{
	int r,c;

 	for (r = 0; r < m; ++r)
	{
		printf("|\t");

		for (c = 0; c < n; ++c)
		{
#ifdef zfp
			printf("%lf\t", (double)matrix(r,c));
#else
			printf("%lf\t", (double)matrix[r*n + c]);
#endif
		}
		printf("|\n");
	}
}

#ifdef ZFP
void init_mat_value(zfp::array2<DATA_TYPE> A, int A_m, int A_n, DATA_TYPE value)
#else
void init_mat_value(DATA_TYPE A[], int A_m, int A_n, DATA_TYPE value)
#endif
{
	int i,j; 
	for (i = 0; i < A_m; ++i)
		for (j = 0; j < A_n; ++j)
#ifdef ZFP
			A(i,j) = value;
#else
			A[i * A_n + j] = value;
#endif
}

#ifdef ZFP
template <typename T>
T compute_RMSE(zfp::array2<T> matrix)
{
	T element_value = A_VALUE * B_VALUE * MATRIX_WIDTH;
	printf("\n\nelement_value = %lf\n\n",element_value);
	T sumSQ = 0;
	for (typename zfp::array2<T>::iterator it = matrix.begin(); it != matrix.end(); it++)
/*	
	for (int r = 0; r < MATRIX_WIDTH; ++r)
		for (int c = 0; c < MATRIX_WIDTH; ++c)
	*/
	{
		//printf("(%d,%d) = %lf\t%lf\n",it.i(), it.j(), (double)matrix(it.i(),it.j()),(double)element_value);
		//printf("(%d,%d) = %lf\n",it.i(), it.j(), element_value);
		printf("(%d,%d) = %lf\n",it.i(), it.j(), matrix(it.i(),it.j()));
		//printf("(%d,%d) = %lf\t%lf\n",it.i(), it.j(), matrix(it.i(),it.j()), element_value);
		sumSQ += pow(element_value - matrix(it.i(),it.j()), 2);
		//sumSQ += pow((double)element_value - (double)matrix(c,r), 2);
		//printf("\n\nsumSQ = %lf\n\n",sumSQ);
	}

	T rmse =  sqrt(sumSQ / (MATRIX_WIDTH * MATRIX_WIDTH));
	printf("\n\nrmse = %lf\n\n", rmse);
	return rmse;
}
#endif




int main()
{
	using namespace zfp;
 	array2<DATA_TYPE> A(MATRIX_WIDTH, MATRIX_WIDTH, RATE, 0, CSIZE);
		//B(MATRIX_WIDTH, MATRIX_WIDTH, RATE, 0, CSIZE),
		//AB(MATRIX_WIDTH, MATRIX_WIDTH, RATE, 0, CSIZE);
	
	// initialize values
	init_mat_value(A, MATRIX_WIDTH, MATRIX_WIDTH, (DATA_TYPE)A_VALUE);
	//init_mat_value(B, MATRIX_WIDTH, MATRIX_WIDTH, (DATA_TYPE)B_VALUE);

	printf("A\n");
	print_matrix(A,MATRIX_WIDTH,MATRIX_WIDTH);
	//printf("B\n");
	//print_matrix(B,MATRIX_WIDTH,MATRIX_WIDTH);

}




